import { CloudFrontRequestCallback, CloudFrontRequestEvent } from 'aws-lambda';

export async function handler(event: CloudFrontRequestEvent, callback: CloudFrontRequestCallback) {
    const request = event.Records[0].cf.request;

    // Incoming URLs from ci.opensearch.org will have a '/ci/123/' prefix, remove the prefix path from requests into S3.
    request.uri = request.uri.replace(/^\/ci\/...\//, '\/');

    console.log('the new request is ', request);

    callback(null, request);
}