import { ArnPrincipal } from '@aws-cdk/aws-iam';
import {
  CfnParameter, Construct, Stack, StackProps,
} from '@aws-cdk/core';
import { ArtifactsPublicAccess } from './artifacts-public-access';
import { Buckets } from './buckets';
import { Identities } from './identities';

export interface BuildArtifactStackProps extends StackProps {
  useExistingBucketAndRoles: boolean,
}

export class BuildArtifactStack extends Stack {
  constructor(scope: Construct, id: string, props: BuildArtifactStackProps) {
    super(scope, id, props);

    const buildAgentPrincipleParam = new CfnParameter(this, 'buildAgentRoleArn', {
      description: 'The role arn of the build agent',
      allowedPattern: '.+',
    });

    let buildBucket;
    if (props.useExistingBucketAndRoles) {
      const buildBucketParam = new CfnParameter(this, 'buildBucketArn', {
        description: 'The arn of the existing build bucket',
        allowedPattern: '.+',
      });
      buildBucket = buildBucketParam.valueAsString;
    }

    const buckets = new Buckets(this, buildBucket);

    const identities = new Identities(this, {
      buildBucket: buckets.BuildBucket,
      useExistingRoles: props.useExistingBucketAndRoles,
      buildAgentPrinciple: new ArnPrincipal(buildAgentPrincipleParam.valueAsString),
    });

    const artifactPublicAccess = new ArtifactsPublicAccess(this, buckets.BuildBucket, props.useExistingBucketAndRoles);
  }
}
