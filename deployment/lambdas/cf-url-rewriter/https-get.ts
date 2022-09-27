/*
* Copyright OpenSearch Contributors  
* SPDX-License-Identifier: Apache-2.0
* 
* The OpenSearch Contributors require contributions made to
* this file be licensed under the Apache-2.0 license or a
*  compatible open source license.
*/

import * as https from 'https';

export async function httpsGet(url: string) {

    return new Promise((resolve, reject) => {

        const request = https.get(url, (res) => {

            let body = "";

            res.on("data", (chunk) => {
                body += chunk;
            });

            res.on("end", () => {
                try {
                    let json = JSON.parse(body);
                    resolve(json);
                } catch (e) {
                    console.log(e);
                    reject({
                        error: 'Failed to parse body!'
                    });
                };
            });
        });

        request.on("error", (e) => {
            console.log(e);
            reject({
                error: 'Request error!'
            });
        });
    });
}
