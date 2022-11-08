#!/usr/bin/env node
/* Copyright OpenSearch Contributors
SPDX-License-Identifier: Apache-2.0

The OpenSearch Contributors require contributions made to
this file be licensed under the Apache-2.0 license or a
compatible open source license. */

import 'source-map-support/register';
import { App } from 'aws-cdk-lib';
import { OsClusterEntrypoint } from '../lib/os-cluster-entrypoint';

const app = new App();

new OsClusterEntrypoint(app, {
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
});
