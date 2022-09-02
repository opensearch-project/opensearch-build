/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class RunIntegTestScriptLibTester extends LibFunctionTester {

    private String jobName
    private String componentName
    private String buildManifest
    private String testManifest
    private String localPath

    public RunIntegTestScriptLibTester(jobName, componentName, buildManifest, testManifest, localPath){
        this.jobName = jobName
        this.componentName = componentName
        this.buildManifest = buildManifest
        this.testManifest = testManifest
        this.localPath = localPath
    }

    void configure(helper, binding) {
        binding.setVariable('env', ['BUILD_NUMBER': '987'])
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.componentName.first(), notNullValue())
        assertThat(call.args.buildManifest.first(), notNullValue())
        assertThat(call.args.testManifest.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.jobName.first().toString().equals(this.jobName)
                && call.args.componentName.first().toString().equals(this.componentName)
                && call.args.buildManifest.first().toString().equals(this.buildManifest)
                && call.args.testManifest.first().toString().equals(this.testManifest)
    }

    String libFunctionName() {
        return 'runIntegTestScript'
    }
}
