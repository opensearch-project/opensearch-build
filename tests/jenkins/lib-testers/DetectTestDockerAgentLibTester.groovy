import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class DetectTestDockerAgentLibTester extends LibFunctionTester {

    private String testManifest

    public DetectTestDockerAgentLibTester(testManifest){
        this.testManifest = testManifest
    }

    void configure(helper, binding) {
        // N/A
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.testManifest.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.testManifest.first().toString().equals(this.testManifest)
    }

    String libFunctionName() {
        return 'detectTestDockerAgent'
    }
}
