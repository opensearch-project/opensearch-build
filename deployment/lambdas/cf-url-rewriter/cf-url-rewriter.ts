import { CloudFrontRequestCallback, CloudFrontRequestEvent } from 'aws-lambda';

export async function handler(event: CloudFrontRequestEvent, callback: CloudFrontRequestCallback) {
    const request = event.Records[0].cf.request;
    request.uri = request.uri.replace(/^\/ci\/...\//, '\/');

    console.log('the new request is ', request);

    callback(null, request);
}