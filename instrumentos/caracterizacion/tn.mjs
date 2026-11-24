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


const { resolve } = await import('node:path');
const { pathToFileURL } = await import('node:url');
const engine = resolve(process.argv[2]);
const { computeStats } = await import(pathToFileURL(resolve(engine, 'gamma.ts')));
const { predictMeanReverting } = await import(pathToFileURL(resolve(engine, 'theories.ts')));

const base = [100, 103, 99, 104, 100, 103, 99, 104, 100, 103, 99, 104, 100, 103, 99, 104, 100, 103, 99, 104, 100];
const variant = process.argv[3] ?? 'base';
assert.ok(['base', 'shifted'].includes(variant));
if (variant === 'shifted') base[base.length - 1] = 102;
const factor = 2;
const series = [base, base.map(value => value * factor)];
const stats = series.map(computeStats);
const alpha = h => Math.max(0, Math.min(1, -h.autocorr[0]));
const near = (a, b) => Math.abs(a - b) <= 1e-10 + 1e-9 * Math.max(Math.abs(a), Math.abs(b));
assert.ok(near(stats[0].mean, stats[1].mean));
assert.ok(near(stats[0].autocorr[0], stats[1].autocorr[0]));
assert.ok(alpha(stats[0]) > 0);
if (variant === 'shifted') assert.ok(!near(stats[0].mean, 0));

function priceCenterControl(h, values) {
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  return mean + alpha(h) * (mean - values.at(-1));
}

function check(role, predict) {
  const [prediction, scaledPrediction] = series.map((values, index) => predict(stats[index], values));
  const expectedScaledPrediction = prediction * factor;
  assert.ok([prediction, scaledPrediction, expectedScaledPrediction].every(Number.isFinite));
  return {
    role,
    passes: near(scaledPrediction, expectedScaledPrediction),
    observed: { prediction, scaledPrediction, expectedScaledPrediction },
  };
}

console.log(JSON.stringify({
  inputs: { base, factor, alpha: stats.map(alpha), meanLogReturn: stats.map(h => h.mean) },
  cases: [
    check('positive', priceCenterControl),
    check('negative', (h, values) => priceCenterControl(h, values) + 1),
    check('candidate', predictMeanReverting),
  ],
}));
