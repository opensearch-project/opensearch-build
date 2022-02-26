import { CloudFrontRequest, CloudFrontRequestCallback, CloudFrontRequestEvent, Context } from 'aws-lambda';

import * as https from 'https'

export async function process(request: CloudFrontRequest, callback: CloudFrontRequestCallback) {
    if (request.uri.includes("/latest/")) {

        const indexUri = request.uri.replace(/\/latest\/.*/, '/index.json');

        try {

            const data: any = await httpGet('https://' + request.headers.host[0].value + indexUri);

            if (data && data.latest) {
                callback(null, redirectResponse(request, data.latest));
            } else {
                callback(null, errorResponse());
            }
        } catch (e) {
            console.error(e);
            callback(null, errorResponse());
        }

    } else {
        // Incoming URLs from ci.opensearch.org will have a '/ci/123/' prefix, remove the prefix path from requests into S3.
        request.uri = request.uri.replace(/^\/ci\/...\//, '\/');
        callback(null, request);
    }
}

export async function handler(event: CloudFrontRequestEvent, context: Context, callback: CloudFrontRequestCallback) {
    const request = event.Records[0].cf.request;

    process(request, callback);
}

export function redirectResponse(request: CloudFrontRequest, latestNumber: number) {
    return {
        status: '302',
        statusDescription: 'Moved temporarily',
        headers: {
            'location': [{
                key: 'Location',
                value: request.uri.replace(/\/latest\//, '/' + latestNumber + '/'),
            }],
            'cache-control': [{
                key: 'Cache-Control',
                value: "max-age=3600"
            }],
        },
    };

}

export function errorResponse() {
    return {
        body: 'The page is not found!',
        status: '404',
        statusDescription: 'Not found',
    };
}

async function httpGet(url: string) {
    return new Promise((resolve, reject) => {

        https.get(url, (res) => {
            let body = "";

            res.on("data", (chunk) => {
                body += chunk;
            });

            res.on("end", () => {
                try {
                    let json = JSON.parse(body);

                    console.log("json ", json);
                    resolve(json);

                    // do something with JSON
                } catch (error) {
                    console.error(error.message);
                    reject(error);
                };
            });

        }).on("error", (error) => {
            console.error(error.message);
            reject(error);

        });
    });
}