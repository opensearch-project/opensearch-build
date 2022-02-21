import { CloudFrontRequest, CloudFrontRequestCallback, CloudFrontRequestEvent, Context } from 'aws-lambda';

export const handle = (request: CloudFrontRequest) => {
    // Incoming URLs from ci.opensearch.org will have a '/ci/123/' prefix, remove the prefix path from requests into S3.
    request.uri = request.uri.replace(/^\/ci\/...\//, '\/');
}

export async function handler(event: CloudFrontRequestEvent, context: Context, callback: CloudFrontRequestCallback) {
    const request = event.Records[0].cf.request;

    handle(request);

    callback(null, request);
}