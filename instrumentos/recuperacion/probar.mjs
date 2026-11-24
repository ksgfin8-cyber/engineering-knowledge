import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdtempSync, readFileSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { registerHooks, stripTypeScriptTypes } from 'node:module';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const symbol = 'SYNTH';
const cutId = 3;
const close = [101, 102, 103, 104, 105, 106];
const warmup = Array.from({ length: 20 }, (_, i) => 100 + (i % 4 === 1 ? 3 : i % 4 === 2 ? -2 : 0));
const source = resolve(process.argv[2]);
const mode = process.argv[3] ?? 'all';

function makeEvents(closes) {
  const prices = [...warmup, ...closes];
  return closes.map((_, index) => ({ id: index + 1, confirmed: true, prices: prices.slice(index, index + 21) }));
}

const clean = makeEvents(close);
function revised(event) {
  return { ...event, prices: [...event.prices.slice(0, -1), event.prices.at(-1) + 7] };
}
const noisy = [clean[0], { ...revised(clean[1]), confirmed: false }, clean[1], revised(clean[1]),
  ...clean.slice(2)];

function json(value) {
  return JSON.stringify(value, (_, item) => {
    if (typeof item === 'number') assert.ok(Number.isFinite(item), 'Número fuera del dominio JSON');
    return item;
  });
}

const digest = value => createHash('sha256').update(json(value)).digest('hex');
const copy = value => JSON.parse(json(value));

async function model(kind) {
  if (kind === 'accumulator') {
    let state = { tick: 0, sum: 0 };
    return {
      step(event) {
        state.tick++;
        state.sum += event.prices.at(-1);
        return { sum: state.sum };
      },
      state: () => state,
      restore: snapshot => { state = snapshot; },
    };
  }
  registerHooks({
    resolve(specifier, context, next) {
      if (specifier.startsWith('@/')) {
        return next(pathToFileURL(resolve(source, 'src', specifier.slice(2) + '.ts')).href, context);
      }
      if (specifier.startsWith('.') && !/\.[a-z]+$/i.test(specifier)) return next(specifier + '.ts', context);
      return next(specifier, context);
    },
    load(url, context, next) {
      if (!url.startsWith('file:') || !url.endsWith('.ts')) return next(url, context);
      const contents = readFileSync(new URL(url), 'utf8');
      const adjusted = contents.replace(/^import\s*\{([^}]+)\}\s*from\s*(['"])(\.[^'"]+)\2;?/gm,
        (_, bindings, quote, path) => {
          const dependency = readFileSync(new URL(path + '.ts', url), 'utf8');
          const types = new Set([...dependency.matchAll(/^export\s+(?:interface|type)\s+(\w+)/gm)].map(m => m[1]));
          const names = bindings.split(',').map(name => name.trim())
            .filter(name => name && !types.has(name.split(/\s+/)[0]));
          return names.length ? `import { ${names.join(', ')} } from ${quote}${path}${quote};` : '';
        });
      return { format: 'module', source: stripTypeScriptTypes(adjusted, { mode: 'transform' }), shortCircuit: true };
    },
  });
  const client = await import(pathToFileURL(resolve(source, 'src/lib/tn-engine/client.ts')));
  return {
    step(event) {
      const candles = event.prices.map((price, index) => ({
        timestamp: (event.id + index) * 60_000, open: price, high: price, low: price, close: price, volume: 1,
      }));
      return client.computeObservables(symbol, candles);
    },
    state: () => client.getTheoryState(symbol) ?? null,
    restore: snapshot => client.getAllTheoryStates().set(symbol, snapshot),
  };
}

function commit(file, journal) {
  const stage = join(dirname(file), 'staged.json');
  writeFileSync(stage, json(journal));
  renameSync(stage, file);
}

async function worker() {
  const [kind, strategy, file, fixture, fault = 'none'] = process.argv.slice(4);
  const engine = await model(kind);
  const journal = existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : { kind, strategy, entries: [] };
  assert.equal(journal.kind, kind);
  assert.equal(journal.strategy, strategy);
  assert.ok(journal.entries.every(({ sequence, input }, i, entries) =>
    sequence === i + 1 && input.confirmed && (!i || input.id > entries[i - 1].input.id)), 'Secuencia de registro inválida');
  let replayed = 0;
  if (journal.entries.length && fault !== 'forget') {
    if (strategy === 'snapshot') {
      assert.equal(journal.snapshot.tick, journal.entries.length, 'Instantánea desacoplada del registro');
      assert.equal(digest(journal.snapshot), journal.entries.at(-1).stateHash);
      engine.restore(journal.snapshot);
    } else {
      for (const { input, observed, stateHash } of journal.entries) {
        assert.deepEqual(engine.step(input), observed);
        assert.equal(digest(engine.state()), stateHash);
        replayed++;
      }
    }
  }
  const fixtures = { clean, noisy, altered: makeEvents([...close.slice(0, 3), 120, 122, 124]) };
  let rejected = 0;
  for (const input of fixtures[fixture]) {
    const lastId = journal.entries.at(-1)?.input.id ?? 0;
    if (!input.confirmed || input.id <= lastId) {
      if (fault === 'late') engine.step(input);
      rejected++;
      continue;
    }
    const observed = engine.step(input);
    if (input.id === cutId && fault === 'before') process.exit(73);
    const state = copy(engine.state());
    journal.entries.push({ sequence: journal.entries.length + 1, input, observed, stateHash: digest(state) });
    if (strategy === 'snapshot') journal.snapshot = state;
    commit(file, journal);
    if (input.id === cutId && fault === 'after') process.exit(73);
  }
  console.log(json({ replayed, rejected, state: engine.state(), entries: journal.entries }));
}

function compare(expected, observed) {
  const firstRow = expected.entries.findIndex((row, i) => digest(row) !== digest(observed.entries[i] ?? null));
  return {
    firstDivergentSequence: firstRow === -1 ? null : firstRow + 1,
    sameTrace: digest(expected.entries) === digest(observed.entries),
    sameState: digest(expected.state) === digest(observed.state),
  };
}

function runCase(kind) {
  const root = mkdtempSync(join(tmpdir(), 'ks006-'));
  try {
    function run(label, strategy, fixture, fault, expectedExit = 0) {
      const file = join(root, label + '.json');
      const child = spawnSync(process.execPath, ['--disable-warning=ExperimentalWarning',
        fileURLToPath(import.meta.url), source, 'worker', kind, strategy, file, fixture, fault ?? 'none'],
      { encoding: 'utf8', timeout: 3000 });
      assert.equal(child.status, expectedExit, child.stderr || String(child.error ?? child.signal ?? ''));
      if (expectedExit) return child.stderr;
      return JSON.parse(child.stdout);
    }
    const stored = label => JSON.parse(readFileSync(join(root, label + '.json'), 'utf8'));
    const baseline = run('baseline', 'replay', 'clean');
    assert.deepEqual(baseline.entries.map(row => row.input.id), [1, 2, 3, 4, 5, 6]);
    if (kind === 'accumulator') {
      assert.deepEqual(baseline.entries.map(row => row.observed.sum), [101, 203, 306, 410, 515, 621]);
    }
    const noCut = run('noise', 'replay', 'noisy');
    assert.equal(noCut.rejected, 2);
    const noise = compare(baseline, noCut);
    assert.ok(noise.sameState && noise.sameTrace);
    const altered = run('future', 'replay', 'altered');
    assert.deepEqual(altered.entries.slice(0, 3), baseline.entries.slice(0, 3));
    assert.notEqual(digest(altered.entries), digest(baseline.entries));

    const recoveries = [];
    for (const strategy of ['replay', 'snapshot']) {
      for (const [cut, count] of [['before', 2], ['after', 3]]) {
        const label = strategy + '-' + cut;
        run(label, strategy, 'noisy', cut, 73);
        assert.equal(stored(label).entries.length, count);
        const resumed = run(label, strategy, 'noisy');
        assert.equal(resumed.replayed, strategy === 'replay' ? count : 0);
        const match = compare(baseline, resumed);
        assert.ok(match.sameState && match.sameTrace);
        recoveries.push({ strategy, cut, committedAtRestart: count, replayed: resumed.replayed,
          bytes: Buffer.byteLength(json(stored(label))), ...match });
      }
    }

    run('forget', 'replay', 'noisy', 'after', 73);
    const forgotten = compare(baseline, run('forget', 'replay', 'noisy', 'forget'));
    assert.ok(!forgotten.sameState && !forgotten.sameTrace);
    const late = compare(baseline, run('late', 'replay', 'noisy', 'late'));
    assert.ok(!late.sameState && !late.sameTrace);
    const damaged = stored('snapshot-after');
    damaged.entries.pop();
    writeFileSync(join(root, 'damaged.json'), json(damaged));
    assert.match(run('damaged', 'snapshot', 'noisy', 'none', 1), /Instantánea desacoplada/);

    return { noise, unchangedPrefix: 3, recoveries, controls: { late, forgotten, missingEntryDetected: true },
      stateFields: Object.keys(baseline.state), finalTick: baseline.state.tick,
      observations: baseline.entries.map(row => row.observed),
      ...(kind === 'accumulator' ? { finalSum: baseline.state.sum } : {
        actualTheoryChanges: baseline.entries.filter(row => row.observed.theoryChanged).length,
      }) };
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

if (mode === 'worker') {
  await worker();
} else {
  assert.ok(['accumulator', 'all'].includes(mode));
  const accumulator = runCase('accumulator');
  if (mode === 'accumulator') console.log(json(accumulator));
  else {
    const lab2 = runCase('lab2');
    console.log(json({
      inputs: { symbol, warmup, close, crashEventId: cutId, scenario: 'LAB2 observer adapter plus admission and journal' },
      cases: [
        { role: 'positive', passes: true, observed: accumulator },
        { role: 'negative', passes: false, observed: lab2.controls },
        { role: 'candidate', passes: true, observed: lab2 },
      ],
    }));
  }
}
