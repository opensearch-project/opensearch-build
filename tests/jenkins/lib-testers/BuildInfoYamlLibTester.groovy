/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class BuildInfoYamlLibTester extends LibFunctionTester {

    private String componentName
    private String inputManifest
    private String outputFile
    private String status
    private String stage

    public BuildInfoYamlLibTester(componentName, inputManifest, outputFile, status, stage){
        this.componentName = componentName
        this.inputManifest = inputManifest
        this.outputFile = outputFile
        this.status = status
        this.stage = stage
    }

    void configure(helper, binding) {
        binding.setVariable('BUILD_NUMBER', '123')
        helper.registerAllowedMethod("writeYaml", [Map.class], {c -> })
        helper.addShMock("git rev-parse HEAD") { script ->
            return [stdout: "75eccfe03b4e58ede1a69eb6008196c44e7008c6", exitValue: 0]
        }
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.inputManifest.first(), notNullValue())
        assertThat(call.args.outputFile.first(), notNullValue())
        assertThat(call.args.status.first(), notNullValue())
        assertThat(call.args.stage.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.inputManifest.first().toString().equals(this.inputManifest)
                && call.args.outputFile.first().toString().equals(this.outputFile)
                && call.args.status.first().toString().equals(this.status)
                && call.args.stage.first().toString().equals(this.stage)
    }

    String libFunctionName() {
        return 'buildInfoYaml'
    }
}
