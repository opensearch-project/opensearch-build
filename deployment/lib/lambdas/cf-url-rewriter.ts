import { CloudFrontRequestEvent, CloudFrontRequest } from 'aws-lambda';

const https = require('https');

export async function handler(event: CloudFrontRequestEvent, context, callback): Promise<CloudFrontRequest> {
  const request = event.Records[0].cf.request;

  if (request.uri.includes("/latest/")) {

    const indexUri = request.uri.replace(/\/latest\/.*/, 'dist/index.json');

    const data = await httpGet('https://' + request.headers.host[0].value + indexUri);

    const redirectResponse = {
      status: '302',
      statusDescription: 'Moved temporarily',
      headers: {
        'location': [{
          key: 'Location',
          value: request.uri.replace('latest', data.latest),
        }],
        'cache-control': [{
          key: 'Cache-Control',
          value: "max-age=3600"
        }],
      },
    };

    console.log('update request', redirectResponse);

    callback(null, redirectResponse);
  } else {
    request.uri = request.uri.replace(/^\/ci\/...\//, '\/');
    callback(null, request);
  }
}

async function httpGet(url) {
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
