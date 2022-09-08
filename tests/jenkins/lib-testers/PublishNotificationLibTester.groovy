/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class PublishNotificationLibTester extends LibFunctionTester {

    private String icon
    private String message
    private String credentialsId
    private String manifest
    private String extra

    public PublishNotificationLibTester(icon, message, extra, manifest, credentialsId) {
        this.icon = icon
        this.message = message
        this.extra = extra
        this.manifest = manifest
        this.credentialsId = credentialsId
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.message.first(), notNullValue())
        assertThat(call.args.credentialsId.first(), notNullValue())
        assertThat(call.args.icon.first(), notNullValue())
        assertThat(call.args.manifest.first(), notNullValue())
        assertThat(call.args.extra.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.message.first().toString().equals(this.message)
                && call.args.credentialsId.first().toString().equals(this.credentialsId)
                && call.args.icon.first().toString().equals(this.icon)
                && call.args.manifest.first().toString().equals(this.manifest)
                && call.args.extra.first().toString().equals(this.extra)
    }

    String libFunctionName() {
        return 'publishNotification'
    }

    void configure(helper, binding){
        binding.setVariable('JOB_NAME', 'dummy_job')
        binding.setVariable('BUILD_NUMBER', '123')
        binding.setVariable('BUILD_URL', 'htth://BUILD_URL_dummy.com')
        binding.setVariable('WEBHOOK_URL', 'htth://WEBHOOK_URL_dummy.com')
        helper.registerAllowedMethod("withCredentials", [Map])
    }
}
