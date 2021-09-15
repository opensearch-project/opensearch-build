import { CloudFrontAllowedMethods, CloudFrontWebDistribution, OriginAccessIdentity } from '@aws-cdk/aws-cloudfront';
import { CanonicalUserPrincipal, PolicyStatement } from '@aws-cdk/aws-iam';
import { IBucket } from '@aws-cdk/aws-s3';
import { CfnOutput } from '@aws-cdk/core';
import { JenkinsArtifactStack } from './jenkins-artifact-stack';

export class ArtifactsPublicAccess {
  constructor(stack: JenkinsArtifactStack, buildBucket: IBucket, existingBucketNeedsUpdate: boolean) {
    const originAccessIdentity = new OriginAccessIdentity(stack, 'cloudfront-OAI', {
      comment: `OAI for ${buildBucket.bucketName}`,
    });

    buildBucket.addToResourcePolicy(new PolicyStatement({
      actions: ['s3:GetObject'],
      resources: [buildBucket.arnForObjects('*')],
      principals: [new CanonicalUserPrincipal(originAccessIdentity.cloudFrontOriginAccessIdentityS3CanonicalUserId)],
    }));

    const distro = new CloudFrontWebDistribution(stack, 'CloudFrontBuildBucket', {
      originConfigs: [
        {
          s3OriginSource: {
            s3BucketSource: buildBucket,
            originAccessIdentity,
          },
          behaviors: [
            {
              isDefaultBehavior: true,
              compress: true,
              allowedMethods: CloudFrontAllowedMethods.GET_HEAD,
            },
          ],
        },
      ],
    });

    new CfnOutput(stack, 'BuildDistributionDomainName', {
      value: distro.distributionDomainName,
      description: 'The domain name where the build artifacts will be available',
    });

    if (existingBucketNeedsUpdate) {
      new CfnOutput(stack, 'OriginAccessIdentityS3Identifier', {
        value: originAccessIdentity.cloudFrontOriginAccessIdentityS3CanonicalUserId,
        description: 'If this account had an S3 bucket, post deployment the buckets resource policy updating, see https://amzn.to/3AtvhBH',
      });
    }
  }
}
