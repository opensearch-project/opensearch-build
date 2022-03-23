import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat
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
