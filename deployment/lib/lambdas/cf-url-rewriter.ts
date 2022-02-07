import { CloudFrontRequestEvent, CloudFrontRequest } from 'aws-lambda';

const aws = require('aws-sdk');

const s3 = new aws.S3({ apiVersion: '2006-03-01' });

export async function handler(event: CloudFrontRequestEvent): Promise<CloudFrontRequest> {
  const { request } = event.Records[0].cf;
  request.uri = request.uri.replace(/^\/ci\/...\//, '/');

  // Below is the working in progress logic to get the max build number under a version with pagination support.
  // Hardcode the version to be 1.7.1 and bucket name to test-access-1-20 for demo purpose.
  console.log('Received event:', JSON.stringify(event, null, 2));

  const bucket = 'test-access-1-20';

  const bucketParams = {
    Bucket: bucket,
    Prefix: '1.7.1/',
    Delimiter: '/',
    ContinuationToken: undefined,
  };

  try {
    let isTruncated = true;
    let continuationToken = null;

    const commonPrefixesAll = [];

    while (isTruncated) {
      if (continuationToken) {
        bucketParams.ContinuationToken = continuationToken;
      }

      const s3Response = s3.listObjectsV2(bucketParams).promise();
      const commonPrefixes = s3Response.CommonPrefixes;

      commonPrefixesAll.push(...commonPrefixes);

      isTruncated = s3Response.IsTruncated;
      continuationToken = s3Response.NextContinuationToken;
    }

    let maxBuildNumber = 0;

    commonPrefixesAll.forEach((prefix) => {
      // e.g '1.7.1/21/'
      const value = prefix.Prefix;

      const reg = /\/(\d+)/;
      const result = value.match(reg);

      if (result) {
        const number = parseInt(result[1], 10);
        if (number > maxBuildNumber) {
          maxBuildNumber = number;
        }
      }
    });

    console.log('maxBuildNumber', maxBuildNumber);
  } catch (ex) {
    console.error(ex);
  }
  return request;
}
