/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import org.yaml.snakeyaml.Yaml


class DetectTestDockerAgentLibTester extends LibFunctionTester {

    private String testManifest

    public DetectTestDockerAgentLibTester(testManifest=null){
        this.testManifest = testManifest
    }

    void configure(helper, binding) {
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((this.testManifest ?: binding.getVariable('TEST_MANIFEST') as File).text)
        })
    }

    void parameterInvariantsAssertions(call) {
        // NA
    }

    boolean expectedParametersMatcher(call) {
        return this.testManifest != null ? call.args.testManifest.first().toString().equals(this.testManifest) : true
    }

    String libFunctionName() {
        return 'detectTestDockerAgent'
    }
}
