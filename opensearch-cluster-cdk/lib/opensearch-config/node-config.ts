/* Copyright OpenSearch Contributors
SPDX-License-Identifier: Apache-2.0

The OpenSearch Contributors require contributions made to
this file be licensed under the Apache-2.0 license or a
compatible open source license. */

export const nodeConfig = new Map<string, object>();

nodeConfig.set('manager', {
  'node.name': 'manager-node',
  'node.master': true,
  'node.data': false,
  'node.ingest': false,
});

nodeConfig.set('data', {
  'node.name': 'data-node',
  'node.master': false,
  'node.data': true,
  'node.ingest': true,
});

nodeConfig.set('seed-manager', {
  'node.name': 'seed',
  'node.master': true,
  'node.data': false,
  'node.ingest': false,
});

nodeConfig.set('seed-data', {
  'node.name': 'seed',
  'node.master': true,
  'node.data': true,
  'node.ingest': false,
});

nodeConfig.set('client', {
  'node.name': 'client-node',
  'node.master': false,
  'node.data': false,
  'node.ingest': false,
});
