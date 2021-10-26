import {
  CloudFrontAllowedMethods, CloudFrontWebDistribution, LambdaEdgeEventType, OriginAccessIdentity,
} from '@aws-cdk/aws-cloudfront';
import { CanonicalUserPrincipal, PolicyStatement } from '@aws-cdk/aws-iam';
import { Code, Function, Runtime } from '@aws-cdk/aws-lambda';
import { IBucket } from '@aws-cdk/aws-s3';
import { CfnOutput } from '@aws-cdk/core';
import { BuildArtifactStack } from './build-artifact-stack';

export class ArtifactsPublicAccess {
  constructor(stack: BuildArtifactStack, buildBucket: IBucket, existingBucketNeedsUpdate: boolean) {
    const originAccessIdentity = new OriginAccessIdentity(stack, 'cloudfront-OAI', {
      comment: `OAI for ${buildBucket.bucketName}`,
    });

    buildBucket.addToResourcePolicy(new PolicyStatement({
      actions: ['s3:GetObject'],
      resources: [buildBucket.arnForObjects('*')],
      principals: [new CanonicalUserPrincipal(originAccessIdentity.cloudFrontOriginAccessIdentityS3CanonicalUserId)],
    }));

    // Incoming URLs from ci.opensearch.org will have a '/ci/123/' prefix, remove the prefix path from requests into S3.
    const urlRewriter = new Function(stack, 'CfUrlRewriter', {
      code: Code.fromInline(`
      exports.handler = (event, context, callback) => {
        const request = event.Records[0].cf.request;
        request.uri = request.uri.replace(/^\\/ci\\/...\\//, '\\/')
        callback(null, request);
      };`),
      handler: 'index.handler',
      runtime: Runtime.NODEJS_14_X,
    });

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
              lambdaFunctionAssociations: [{
                eventType: LambdaEdgeEventType.VIEWER_REQUEST,
                lambdaFunction: urlRewriter.currentVersion,
              }],
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
