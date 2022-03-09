import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class RunIntegTestScriptLibTester extends LibFunctionTester {

    private String jobName
    private String buildManifest
    private String testManifest
    private String buildId

    public RunIntegTestScriptLibTester(jobName, buildManifest, testManifest, buildId){
        this.jobName = jobName
        this.buildManifest = buildManifest
        this.testManifest = testManifest
        this.buildId = buildId
    }

    void configure(helper, binding) {
        // N/A
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.buildManifest.first(), notNullValue())
        assertThat(call.args.testManifest.first(), notNullValue())
        assertThat(call.args.buildId.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.jobName.first().toString().equals(this.jobName)
                && call.args.buildManifest.first().toString().equals(this.buildManifest)
                && call.args.testManifest.first().toString().equals(this.testManifest)
                && call.args.buildId.first().toString().equals(this.buildId)
    }

    String libFunctionName() {
        return 'runIntegTestScript'
    }
}
