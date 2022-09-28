/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class BuildYumRepoTester extends LibFunctionTester {

    private String buildManifest
    private String baseUrl

    public BuildYumRepoTester(buildManifest, baseUrl) {
        this.buildManifest = buildManifest
        this.baseUrl = baseUrl
    }

    void configure(helper, binding) {
        binding.setVariable('BUILD_NUMBER', '123')

        helper.registerAllowedMethod("writeFile", [Map])
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.buildManifest.first(), notNullValue())
        assertThat(call.args.baseUrl.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.buildManifest.first().toString().equals(this.buildManifest) &&
            call.args.baseUrl.first().toString().equals(this.baseUrl)
    }

    String libFunctionName() {
        return 'buildYumRepo'
    }

}
