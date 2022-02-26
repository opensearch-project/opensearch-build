import { CloudFrontRequest } from 'aws-lambda';
import { handle } from "../../../lambdas/cf-url-rewriter/cf-url-rewriter";

test('Lmabda handle uri with ci string', () => {

    let request = { uri: '/ci/dbc/bundle-build-dashboards/1.2.0/428/linux/x64/' } as CloudFrontRequest;

    handle(request);

    expect(request.uri).toBe('/bundle-build-dashboards/1.2.0/428/linux/x64/');
});

test('Lmabda handle uri without ci string', () => {

    let request = { uri: '/bundle-build-dashboards/1.2.0/428/linux/x64/' } as CloudFrontRequest;

    handle(request);

    expect(request.uri).toBe('/bundle-build-dashboards/1.2.0/428/linux/x64/');
});