/*
* Copyright OpenSearch Contributors  
* SPDX-License-Identifier: Apache-2.0
* 
* The OpenSearch Contributors require contributions made to
* this file be licensed under the Apache-2.0 license or a
*  compatible open source license.
*/

import { countResources, expect, haveOutput, haveResourceLike, not } from '@aws-cdk/assert';
import { App } from '@aws-cdk/core';
import { BuildArtifactStack } from '../lib/build-artifact-stack';

test('Fresh BuildArtifact Stack', () => {
  const app = new App();

  // WHEN
  const stack = new BuildArtifactStack(app, 'MyTestStack', { useExistingBucketAndRoles: false });

  // THEN
  expect(stack).to(countResources('AWS::S3::Bucket', 1));
  expect(stack).to(countResources('AWS::IAM::Role', 4));
  expect(stack).to(countResources('AWS::CloudFront::CloudFrontOriginAccessIdentity', 1));

  expect(stack).to(countResources('AWS::CloudFront::Distribution', 1));
  expect(stack).to(haveResourceLike('AWS::CloudFront::Distribution', {
    DistributionConfig: {
      DefaultCacheBehavior: {
        DefaultTTL: 300
      }
    }
  }));

  expect(stack).to(countResources('AWS::Lambda::Function', 1));
  expect(stack).to(haveOutput({ outputName: 'BuildDistributionDomainName' }));
  expect(stack).to(not(haveOutput({ outputName: 'OriginAccessIdentityS3Identifier' })));
});

test('Existing BuildArtifact Stack', () => {
  const app = new App();

  // WHEN
  const stack = new BuildArtifactStack(app, 'MyTestStack', { useExistingBucketAndRoles: true });

  // THEN
  expect(stack).to(countResources('AWS::S3::Bucket', 0));
  expect(stack).to(countResources('AWS::IAM::Role', 1));
  expect(stack).to(countResources('AWS::CloudFront::CloudFrontOriginAccessIdentity', 1));

  expect(stack).to(countResources('AWS::CloudFront::Distribution', 1));
  expect(stack).to(haveResourceLike('AWS::CloudFront::Distribution', {
    DistributionConfig: {
      DefaultCacheBehavior: {
        DefaultTTL: 300
      }
    }
  }));

  expect(stack).to(countResources('AWS::Lambda::Function', 1));
  expect(stack).to(haveOutput({ outputName: 'BuildDistributionDomainName' }));
  expect(stack).to(haveOutput({ outputName: 'OriginAccessIdentityS3Identifier' }));
});
