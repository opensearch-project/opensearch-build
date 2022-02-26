import { CloudFrontRequest, CloudFrontRequestCallback } from 'aws-lambda';
import { errorResponse, process, redirectResponse } from "../../../lambdas/cf-url-rewriter/cf-url-rewriter";

test('Lmabda handle uri with ci string', () => {

    // let request = { uri: '/ci/dbc/bundle-build-dashboards/1.2.0/428/linux/x64/' } as CloudFrontRequest;
    // let callback = {} as CloudFrontRequestCallback;

    // process(request, callback);

    // expect(request.uri).toBe('/bundle-build-dashboards/1.2.0/428/linux/x64/');
});

test('errorResponse', () => {
    const response = errorResponse();

    expect(response.body).toBe('The page is not found!');
    expect(response.status).toBe('404');
    expect(response.statusDescription).toBe('Not found');
});

test('redirectResponse', () => {
    let request = { uri: '/ci/dbc/bundle-build-dashboards/1.2.0/latest/linux/x64/' } as CloudFrontRequest;
    const buildNumber = 123;

    const response = redirectResponse(request, buildNumber);
    console.log(response);
    console.log(JSON.stringify(response));


    expect(response.status).toBe('302');
    expect(response.statusDescription).toBe('Moved temporarily');
    expect(response.headers.location).toStrictEqual([{ "key": "Location", "value": "/ci/dbc/bundle-build-dashboards/1.2.0/123/linux/x64/" }]);
    expect(response.headers['cache-control']).toStrictEqual([{ "key": "Cache-Control", "value": "max-age=3600" }]);

});

// test('Lmabda handle uri without ci string', () => {

//     let request = { uri: '/bundle-build-dashboards/1.2.0/428/linux/x64/' } as CloudFrontRequest;

//     handle(request);

//     expect(request.uri).toBe('/bundle-build-dashboards/1.2.0/428/linux/x64/');
// });