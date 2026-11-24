'use strict';
const assert = require('node:assert/strict');
const { resolve } = require('node:path');
const root = resolve(process.argv[2]);
const { config } = require(resolve(root, 'tools/p01/protocol.cjs'));
const { loadRuntime } = require(resolve(root, 'tools/p01/runtime.cjs'));
const runtime = loadRuntime();

const source = state => state.entities.values().next().value;
function terminal(trajectory) {
  const state = trajectory.steps.at(-1).world_state;
  return { ticks: trajectory.steps.length, energy: source(state).energy, reason: trajectory.termination_reason };
}

function contrast(seed, policy) {
  const spec = config(seed, policy);
  const result = runtime.run(spec);
  assert.equal(result.status, 'COMPLETED');
  const trajectory = runtime.realm(result.trajectory);
  const { steps, initial_state, events } = trajectory;
  assert.ok(steps.length >= 3);
  const { api } = runtime;
  const configured = new api.ExperimentConfig(runtime.realm(spec));
  const actions = steps.map(row => row.action);
  const initialEvents = events.slice(0, source(initial_state).lifecycle === 'DEAD' ? 1 : 0);
  const replay = api.replay_trajectory(initial_state, initialEvents, actions, configured.world_config,
    configured.feedback_config, steps.length, configured.max_ticks, 'WITH_AGENT');
  const good = api.validate_replay(trajectory, replay, configured.world_config, 'WITH_AGENT');
  assert.equal(good.status, 'MATCH');

  const changed = runtime.realm(structuredClone(result.trajectory));
  const interior = Math.floor(steps.length / 2);
  source(changed.steps[interior].world_state).energy -= 1;
  assert.deepEqual(terminal(trajectory), terminal(changed));
  const bad = api.validate_replay(changed, replay, configured.world_config, 'WITH_AGENT');
  assert.notEqual(bad.status, 'MATCH');
  const first = replay.records.findIndex((row, i) =>
    source(row.world_state).energy !== source(changed.steps[i].world_state).energy);
  assert.equal(first, interior);
  return { seed, policy, terminal: terminal(trajectory), terminal_unchanged: true,
    clean: good.status, perturbed: bad.status, first_step: first + 1,
    original_energy: source(steps[first].world_state).energy,
    observed_energy: source(changed.steps[first].world_state).energy };
}

const evidence = [1, 2].flatMap(seed => ['wait', 'rule'].map(policy => contrast(seed, policy)));
console.log(JSON.stringify(evidence, (_, value) => typeof value === 'bigint' ? value.toString() : value));
