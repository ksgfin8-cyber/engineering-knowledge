import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { registerHooks, stripTypeScriptTypes } from 'node:module';

registerHooks({
  resolve(specifier, context, next) {
    if (specifier.startsWith('.') && !/\.[a-z]+$/i.test(specifier)) {
      return next(specifier + '.ts', context);
    }
    return next(specifier, context);
  },
  load(url, context, next) {
    if (!url.startsWith('file:') || !url.endsWith('.ts')) return next(url, context);
    const source = readFileSync(new URL(url), 'utf8');
    // These sources use named imports for both TypeScript types and runtime bindings.
    // Elide imports of exported interfaces/type aliases before Node loads the module.
    const adjusted = source.replace(/^import\s*\{([^}]+)\}\s*from\s*(['"])(\.[^'"]+)\2;?/gm,
      (_, bindings, quote, path) => {
        const dependency = readFileSync(new URL(path + '.ts', url), 'utf8');
        const typeNames = new Set([...dependency.matchAll(/^export\s+(?:interface|type)\s+(\w+)/gm)]
          .map(match => match[1]));
        const values = bindings.split(',').map(name => name.trim())
          .filter(name => name && !typeNames.has(name.split(/\s+/)[0]));
        return values.length ? `import { ${values.join(', ')} } from ${quote}${path}${quote};` : '';
      });
    return { format: 'module', source: stripTypeScriptTypes(adjusted, { mode: 'transform' }), shortCircuit: true };
  },
});

import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { performance } from 'node:perf_hooks';

const engine = resolve(process.argv[2]);
const mode = process.argv[3] ?? 'full';
assert.ok(['decision', 'full'].includes(mode));
const { computeStats } = await import(pathToFileURL(resolve(engine, 'gamma.ts')));
const { predict } = await import(pathToFileURL(resolve(engine, 'theories.ts')));

function series(length) {
  return Array.from({ length }, (_, i) => 100 + i * 0.12 + (i % 4 === 1 ? 3 : i % 4 === 2 ? -2 : 0));
}

function independentReference(prices, ids, describe, sharedEnvelope) {
  const envelope = sharedEnvelope ? describe(prices) : null;
  const rows = [];
  for (let origin = 20; origin < prices.length - 1; origin++) {
    for (const theory of ids) {
      const window = prices.slice(origin - 20, origin + 1);
      const forecast = predict(theory, envelope ?? describe(window), window);
      const target = prices[origin + 1];
      rows.push({ origin, targetIndex: origin + 1, theory, forecast, target, absoluteError: Math.abs(forecast - target) });
    }
  }
  return rows;
}

const fixture = series(64);
const altered = fixture.map((value, i) => i < 32 ? value : value + 30 + i * 0.3);
const theories = [0, 1, 2, 3];
const get = (rows, origin, theory) => rows.find(row => row.origin === origin && row.theory === theory);
const envelopeA = independentReference(fixture, theories, computeStats, true);
const envelopeB = independentReference(altered, theories, computeStats, true);
const divergent = envelopeA.filter(row => row.origin <= 31 && row.theory === 1
  && row.forecast !== get(envelopeB, row.origin, row.theory).forecast);
assert.ok(divergent.length > 0);
const first = divergent[0];
const design = { commonPrefix: 32, firstDivergence: first.origin,
  firstTarget: first.target, envelopeForecasts: [first.forecast, get(envelopeB, first.origin, 1).forecast],
  divergentCommonOriginsT1: divergent.length };

if (mode === 'decision') {
  console.log(JSON.stringify(design));
} else {
  const { scoreByOrigin } = await import('./evaluar.mjs');
  const evaluate = (prices, ids, describe = computeStats) => scoreByOrigin(prices, ids, { describe, predict });
  const a = evaluate(fixture, theories);
  const b = evaluate(altered, theories);
  const common = a.filter(row => row.origin <= 31);
  assert.equal(common.length, 48);
  const complete = common.filter(row => row.origin < 31);
  assert.equal(complete.length, 44);
  for (const row of common) {
    const other = get(b, row.origin, row.theory);
    assert.equal(row.forecast, other.forecast);
    if (row.origin < 31) assert.deepEqual(row, other);
    if (row.theory === 0) assert.equal(row.forecast, fixture[row.origin]);
  }
  assert.notEqual(get(a, 31, 0).target, get(b, 31, 0).target);
  assert.throws(() => evaluate(series(21), theories), RangeError);
  assert.throws(() => evaluate(fixture, [1, 1]), RangeError);
  assert.throws(() => evaluate(fixture.map((x, i) => i === 0 ? NaN : x), theories), RangeError);
  assert.throws(() => scoreByOrigin(fixture, theories, { describe: computeStats, predict: () => Infinity }), RangeError);

  const measures = [];
  for (const [size, count] of [[64, 2], [256, 4], [1024, 8]]) {
    const prices = series(size);
    const ids = Array.from({ length: count }, (_, i) => i);
    let referenceCalls = 0;
    let sharedCalls = 0;
    const beforeReference = performance.now();
    const reference = independentReference(prices, ids, w => { referenceCalls++; return computeStats(w); }, false);
    const referenceMs = performance.now() - beforeReference;
    const beforeShared = performance.now();
    const shared = evaluate(prices, ids, w => { sharedCalls++; return computeStats(w); });
    const sharedMs = performance.now() - beforeShared;
    assert.deepEqual(shared, reference);
    assert.equal(referenceCalls, (size - 21) * count);
    assert.equal(sharedCalls, size - 21);
    measures.push({ size, count, rows: shared.length, referenceCalls, sharedCalls });
    console.error(JSON.stringify({ size, count, referenceMs, sharedMs }));
  }

  console.log(JSON.stringify({
    design, causalCommonForecasts: common.length, causalCommonFullRecords: complete.length, invalidCasesDetected: 4, measures,
  }, null, 2));
}
