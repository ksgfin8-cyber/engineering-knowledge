const windowSize = 21;

/**
 * Evalúa pronósticos de nivel a un paso con un descriptor por origen.
 * describe y predict usan el mismo contexto por origen; predict no muta su entrada.
 * El descriptor excluye el objetivo. Su identidad se limita a esta ejecución.
 */
export function scoreByOrigin(prices, theories, { describe, predict }) {
  if (!Array.isArray(prices) || prices.length <= windowSize
      || Array.from(prices).some(value => !Number.isFinite(value) || value <= 0)) {
    throw new RangeError('Se requieren al menos 22 precios finitos y positivos');
  }
  if (!Array.isArray(theories) || theories.length === 0
      || Array.from(theories).some(id => !Number.isInteger(id) || id < 0 || id > 9)
      || new Set(theories).size !== theories.length) {
    throw new RangeError('Se requieren identificadores TN distintos de 0 a 9');
  }

  const rows = [];
  for (let origin = windowSize - 1; origin < prices.length - 1; origin++) {
    const window = prices.slice(origin - windowSize + 1, origin + 1);
    const stats = describe(window);
    const targetIndex = origin + 1;
    const target = prices[targetIndex];
    for (const theory of theories) {
      const forecast = predict(theory, stats, window);
      const absoluteError = Math.abs(forecast - target);
      if (!Number.isFinite(forecast) || !Number.isFinite(absoluteError)) {
        throw new RangeError('Pronóstico o error no finito en origen ' + origin + ', teoría ' + theory);
      }
      rows.push({ origin, targetIndex, theory, forecast, target, absoluteError });
    }
  }
  return rows;
}
