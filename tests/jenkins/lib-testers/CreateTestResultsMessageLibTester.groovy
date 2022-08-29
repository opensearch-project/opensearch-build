/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class CreateTestResultsMessageLibTester extends LibFunctionTester {

    private String testType
    private String status
    private String absoluteUrl

    public CreateTestResultsMessageLibTester(
        String testType,
        String status,
        String absoluteUrl
    ){
        this.testType = testType
        this.status = status
        this.absoluteUrl = absoluteUrl
    }

    void configure(helper, binding) {
        binding.setVariable('STAGE_NAME', 'stage')
        helper.registerAllowedMethod('findFiles', [Map.class], null)
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.testType.first(), notNullValue())
        assertThat(call.args.status.first(), notNullValue())
        assertThat(call.args.absoluteUrl.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.testType.first().toString().equals(this.testType)
                && call.args.status.first().toString().equals(this.status)
                &&  call.args.absoluteUrl.first().toString().equals(this.absoluteUrl)
    }

    String libFunctionName() {
        return 'createTestResultsMessage'
    }
}
