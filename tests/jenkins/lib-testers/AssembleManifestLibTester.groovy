import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class AssembleManifestLibTester extends LibFunctionTester {

    private String buildManifest

    public AssembleManifestLibTester(buildManifest) {
        this.buildManifest = buildManifest
    }

    void configure(helper, binding) {

        binding.setVariable('PUBLIC_ARTIFACT_URL', 'https://ci.opensearch.org/dbc')
        binding.setVariable('JOB_NAME', 'vars-build')
        binding.setVariable('BUILD_NUMBER', '123')
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.buildManifest.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.buildManifest.first().toString().equals(this.buildManifest)
    }

    String libFunctionName() {
        return 'assembleManifest'
    }

}
