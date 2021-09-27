import { AnyPrincipal, Role } from '@aws-cdk/aws-iam';
import { Bucket, IBucket } from '@aws-cdk/aws-s3';

import { JenkinsArtifactStack } from './jenkins-artifact-stack';

export class Buckets {
  readonly BuildBucket: IBucket;

  constructor(stack: JenkinsArtifactStack, buildBucketArn?: string) {
    this.BuildBucket = buildBucketArn
      ? Bucket.fromBucketArn(stack, 'BuildBucket', buildBucketArn)
      : new Bucket(stack, 'BuildBucket', {});
  }
}
