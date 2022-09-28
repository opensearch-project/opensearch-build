/*
* Copyright OpenSearch Contributors
* SPDX-License-Identifier: Apache-2.0
*
* The OpenSearch Contributors require contributions made to
* this file be licensed under the Apache-2.0 license or a
*  compatible open source license.
*/

#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { BuildArtifactStack } from '../lib/build-artifact-stack';

const app = new cdk.App();
new BuildArtifactStack(app, 'ExistingBuildArtifact', {
  useExistingBucketAndRoles: true,
});
new BuildArtifactStack(app, 'BuildArtifactDev', {
  useExistingBucketAndRoles: false,
});
