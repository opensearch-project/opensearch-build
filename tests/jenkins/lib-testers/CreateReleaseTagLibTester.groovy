import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class CreateReleaseTagLibTester extends LibFunctionTester {

    private String buildManifest
    private String tagVersion

    public CreateReleaseTagLibTester(buildManifest, tagVersion){
        this.buildManifest = buildManifest
        this.tagVersion = tagVersion
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.buildManifest.first(), notNullValue())
        assertThat(call.args.tagVersion.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.buildManifest.first().toString().equals(this.buildManifest)
                && call.args.tagVersion.first().toString().equals(this.tagVersion)
    }

    String libFunctionName(){
        return 'createReleaseTag'
    }

    void configure(helper, binding){
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'dummy_token_name')
        binding.setVariable('WORKSPACE', 'tmp/workspace/')
        binding.setVariable('GITHUB_USER', 'dummy_user')
        binding.setVariable('GITHUB_TOKEN', 'dummy_token')
    }
}
