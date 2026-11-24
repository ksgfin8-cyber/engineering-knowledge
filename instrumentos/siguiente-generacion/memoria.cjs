'use strict';
const assert = require('node:assert/strict');
const { resolve } = require('node:path');
const root = resolve(process.argv[2]);
const { config } = require(resolve(root, 'tools/p01/protocol.cjs'));
const { loadRuntime } = require(resolve(root, 'tools/p01/runtime.cjs'));
const runtime = loadRuntime();
const { api } = runtime;

function run(seed, resetEachStep) {
  const settings = { ...config(seed, 'frontier_memory_v1'), max_ticks: 24 };
  const checked = new api.ExperimentConfig(runtime.realm(settings));
  const result = api.run_experiment(checked, () => {
    const agent = new api.FrontierMemoryAgent();
    return {
      reset: () => agent.reset(),
      step(feedback) {
        if (resetEachStep) agent.reset();
        return agent.step(feedback);
      },
    };
  });
  assert.equal(result.status, 'COMPLETED', JSON.stringify(result.failure_details));
  const trajectory = result.trajectory;
  const initial = trajectory.initial_state.entities.values().next().value;
  const events = trajectory.events.slice(0, initial.lifecycle === 'DEAD' ? 1 : 0);
  const replay = api.replay_trajectory(trajectory.initial_state, events, trajectory.steps.map(s => s.action),
    checked.world_config, checked.feedback_config, trajectory.steps.length, checked.max_ticks, 'WITH_AGENT');
  assert.equal(api.validate_replay(trajectory, replay, checked.world_config, 'WITH_AGENT').status, 'MATCH');
  return trajectory;
}

function summary(t) {
  const last = t.steps.at(-1).world_state.entities.values().next().value;
  return { steps: t.steps.length, energy: last.energy,
    consumed: t.events.filter(e => e.type === 'RESOURCE_CONSUMED').length, reason: t.termination_reason };
}

function compare(seed) {
  const retained = run(seed, false);
  const reset = run(seed, true);
  assert.ok(api.replay_values_equal(retained.initial_state, reset.initial_state));
  const feedback = retained.steps[0].feedback;
  const isolated = [new api.FrontierMemoryAgent(), new api.FrontierMemoryAgent()].map(a => a.step(feedback).type);
  assert.equal(isolated[0], isolated[1]);
  assert.equal(retained.steps[0].action.type, reset.steps[0].action.type);
  const first = retained.steps.findIndex((r, i) => i < reset.steps.length && r.action.type !== reset.steps[i].action.type);
  assert.notEqual(first, -1, 'No first divergence in this fixture');
  assert.ok(api.replay_values_equal(retained.steps[first].feedback, reset.steps[first].feedback));
  const prior = first ? retained.steps[first - 1].world_state : retained.initial_state;
  const priorReset = first ? reset.steps[first - 1].world_state : reset.initial_state;
  assert.ok(api.replay_values_equal(prior, priorReset));
  return { seed, isolated_first_actions: isolated, first_different_step: first + 1,
    first_actions: [retained.steps[first].action.type, reset.steps[first].action.type],
    retained: summary(retained), reset: summary(reset), replay: ['MATCH', 'MATCH'] };
}

console.log(JSON.stringify([1, 2].map(compare), (_, v) => typeof v === 'bigint' ? v.toString() : v));
