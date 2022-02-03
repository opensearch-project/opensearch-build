const aws = require('aws-sdk');

const s3 = new aws.S3({ apiVersion: '2006-03-01' });

exports.handler = async (event, context) => {

    const request = event.Records[0].cf.request;
    request.uri = request.uri.replace(/^\/ci\/...\//, '\/')
    callback(null, request);

    // Below is the working in progress logic to get the max build number under a version with pagination support.
    // Hardcode the version to be 1.7.1 and bucket name to test-access-1-20 for demo purpose.
    console.log('Received event:', JSON.stringify(event, null, 2));

    const bucket = "test-access-1-20";

    var bucketParams = {
        Bucket: bucket,
        Prefix: '1.7.1/',
        Delimiter: '/'
    };

    try {

        var isTruncated = true;
        var continuationToken = null;

        var commonPrefixesAll = [];

        while (isTruncated) {

            if (continuationToken) {
                bucketParams.ContinuationToken = continuationToken;
            }

            const s3Response = await s3.listObjectsV2(bucketParams).promise();
            const commonPrefixes = s3Response.CommonPrefixes;

            commonPrefixesAll.push(...commonPrefixes);

            isTruncated = s3Response.IsTruncated;
            continuationToken = s3Response.NextContinuationToken;
        }

        var maxBuildNumber = 0;

        commonPrefixesAll.forEach((prefix) => {
            // e.g '1.7.1/21/'
            const value = prefix['Prefix'];

            const reg = /\/(\d+)/;
            const result = value.match(reg);

            if (result) {
                const number = parseInt(result[1]);
                if (number > maxBuildNumber) {
                    maxBuildNumber = number;
                }
            }
        });

        console.log('maxBuildNumber', maxBuildNumber);
    }
    catch (ex) {
        console.error(ex);
    }
};
