/*
* Copyright OpenSearch Contributors  
* SPDX-License-Identifier: Apache-2.0
* 
* The OpenSearch Contributors require contributions made to
* this file be licensed under the Apache-2.0 license or a
*  compatible open source license.
*/

import { CloudFrontEvent, CloudFrontHeaders, CloudFrontRequest, CloudFrontRequestCallback, CloudFrontRequestEvent, Context } from 'aws-lambda';
import { handler } from '../../../lambdas/cf-url-rewriter/cf-url-rewriter';
import { httpsGet } from '../../../lambdas/cf-url-rewriter/https-get';
jest.mock('../../../lambdas/cf-url-rewriter/https-get');

beforeEach(() => {
    jest.resetAllMocks();
});

test('handler with latest url and valid latest field', async () => {

    const event = createTestEvent('/ci/dbc/bundle-build-dashboards/1.2.0/latest/linux/x64/');
    const context = {} as Context;
    const callback = jest.fn() as CloudFrontRequestCallback;

    (httpsGet as unknown as jest.Mock).mockReturnValue({ latest: '123' });

    await handler(event, context, callback);

    expect(httpsGet).toBeCalledWith('https://test.cloudfront.net/ci/dbc/bundle-build-dashboards/1.2.0/index.json');

    expect(callback).toHaveBeenCalledWith(
        null,
        {
            "headers": {
                "cache-control": [{ "key": "Cache-Control", "value": "max-age=3600" }],
                "location": [{ "key": "Location", "value": "/ci/dbc/bundle-build-dashboards/1.2.0/123/linux/x64/" }]
            },
            "status": "302",
            "statusDescription": "Moved temporarily"
        }
    );
});

test('handler with latest url and empty latest field', async () => {

    const event = createTestEvent('/ci/dbc/bundle-build-dashboards/1.2.0/latest/linux/x64/');
    const context = {} as Context;
    const callback = jest.fn() as CloudFrontRequestCallback;

    (httpsGet as unknown as jest.Mock).mockReturnValue({ latest: '' });

    await handler(event, context, callback);

    expect(httpsGet).toBeCalledWith('https://test.cloudfront.net/ci/dbc/bundle-build-dashboards/1.2.0/index.json');

    expect(callback).toHaveBeenCalledWith(
        null,
        {
            "body": "The page is not found!",
            "status": "404",
            "statusDescription": "Not found"
        }
    );
});

test('handler without latest url and without ci keyword', async () => {

    const event = createTestEvent('/bundle-build-dashboards/1.2.0/456/linux/x64/');
    const context = {} as Context;
    const callback = jest.fn() as CloudFrontRequestCallback;

    (httpsGet as unknown as jest.Mock).mockReturnValue({ latest: '123' });

    await handler(event, context, callback);

    expect(callback).toHaveBeenCalledWith(
        null,
        {
            "body": "The page is not found!",
            "status": "404",
            "statusDescription": "Not found"
        }
    );

    expect(httpsGet).not.toHaveBeenCalled();
})

test('handler with latest url and without ci keyword', async () => {

    const event = createTestEvent('/bundle-build-dashboards/1.2.0/latest/linux/x64/');
    const context = {} as Context;
    const callback = jest.fn() as CloudFrontRequestCallback;

    (httpsGet as unknown as jest.Mock).mockReturnValue({ latest: '' });

    await handler(event, context, callback);

    expect(callback).toHaveBeenCalledWith(
        null,
        {
            "body": "The page is not found!",
            "status": "404",
            "statusDescription": "Not found"
        }
    );

    expect(httpsGet).not.toHaveBeenCalled();
});

test('handler with latest url and exception when getting index.json', async () => {

    const event = createTestEvent('/ci/dbc/bundle-build-dashboards/1.2.0/latest/linux/x64/');
    const context = {} as Context;
    const callback = jest.fn() as CloudFrontRequestCallback;

    (httpsGet as unknown as jest.Mock).mockImplementation(() => {
        throw new Error('Error getting!');
    });

    await handler(event, context, callback);

    expect(httpsGet).toBeCalledWith('https://test.cloudfront.net/ci/dbc/bundle-build-dashboards/1.2.0/index.json');

    expect(callback).toHaveBeenCalledWith(
        null,
        {
            "body": "The page is not found!",
            "status": "404",
            "statusDescription": "Not found"
        }
    );
});

test('handler without latest url', async () => {

    const event = createTestEvent('/ci/dbc/bundle-build-dashboards/1.2.0/456/linux/x64/');
    const context = {} as Context;
    const callback = jest.fn() as CloudFrontRequestCallback;

    (httpsGet as unknown as jest.Mock).mockReturnValue({ latest: '123' });

    await handler(event, context, callback);

    expect(callback).toHaveBeenCalledWith(
        null,
        {
            "headers": { "host": [{ "key": "Host", "value": "test.cloudfront.net" }] },
            "uri": "/bundle-build-dashboards/1.2.0/456/linux/x64/"
        }
    );

    expect(httpsGet).not.toHaveBeenCalled();
})

test('handler with /fool(latest)bar/ keyword', async () => {

    const event = createTestEvent('/ci/dbc/bundle-build-dashboards/1.2.0/456/linux/x64/foollatestbar/');
    const context = {} as Context;
    const callback = jest.fn() as CloudFrontRequestCallback;

    (httpsGet as unknown as jest.Mock).mockReturnValue({ latest: '123' });

    await handler(event, context, callback);

    expect(callback).toHaveBeenCalledWith(
        null,
        {
            "headers": { "host": [{ "key": "Host", "value": "test.cloudfront.net" }] },
            "uri": "/bundle-build-dashboards/1.2.0/456/linux/x64/foollatestbar/"
        }
    );

    expect(httpsGet).not.toHaveBeenCalled();
})

function createTestEvent(uri: string): CloudFrontRequestEvent {
    const event = {} as CloudFrontRequestEvent;

    const headers = {
        "host": [
            {
                "key": "Host",
                "value": "test.cloudfront.net"
            }
        ]
    } as CloudFrontHeaders;

    const request = {
        uri: uri,
        headers: headers

    } as CloudFrontRequest;

    const cf: CloudFrontEvent & {
        request: CloudFrontRequest;
    } = {
        config: {} as CloudFrontEvent["config"],
        request: request
    };

    event.Records = [{ cf: cf }];

    return event;
}
