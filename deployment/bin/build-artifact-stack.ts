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
