/*
* Copyright OpenSearch Contributors  
* SPDX-License-Identifier: Apache-2.0
* 
* The OpenSearch Contributors require contributions made to
* this file be licensed under the Apache-2.0 license or a
*  compatible open source license.
*/

import { ClientRequest } from 'http';
import * as https from 'https';
import { Stream } from 'stream';
import { httpsGet } from '../../../lambdas/cf-url-rewriter/https-get';

jest.mock('https');

beforeEach(() => {
    jest.resetAllMocks();
});

test('httpGet valid json', async () => {

    const stream = new Stream();

    (https.get as unknown as jest.Mock) = jest.fn().mockImplementation((url, cb) => {
        cb(stream);
        stream.emit('data', JSON.stringify({ key: 'value' }));
        stream.emit('end');
    });

    const url = 'https://testurl.com';
    const data = await httpsGet(url);

    expect(data).toStrictEqual({ key: 'value' });
});

test('httpGet invalid json', async () => {
    const stream = new Stream();

    (https.get as unknown as jest.Mock) = jest.fn().mockImplementation((url, cb) => {
        cb(stream);
        stream.emit('data', 'random string');
        stream.emit('end');
    });

    const url = 'https://testurl.com';

    try {
        await httpsGet(url);
    } catch (e) {
        expect(e).toStrictEqual({ error: 'Failed to parse body!' });
    }
});

test('httpGet request on event error', async () => {
    const stream = new Stream();
    const mockGet = {} as ClientRequest;

    mockGet.on = jest.fn().mockImplementation((event, cb) => {
        cb(stream);
        stream.emit('error', 'some error');
    });

    (https.get as unknown as jest.Mock).mockReturnValue(mockGet);

    const url = 'https://testurl.com';

    try {
        await httpsGet(url);
    } catch (e) {
        expect(e).toStrictEqual({ error: 'Request error!' });
    }

});

test('httpGet request error', async () => {
    const error = new Error('Error getting!');

    (https.get as unknown as jest.Mock).mockImplementation(() => {
        throw error;
    });

    const url = 'https://testurl.com';

    try {
        await httpsGet(url);
    } catch (e) {
        expect(e).toBe(error);
    }
});
