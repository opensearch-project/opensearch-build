import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class RunGradleCheckLibTester extends LibFunctionTester {

    private String gitRepoUrl
    private String gitReference

    public RunGradleCheckLibTester(gitRepoUrl, gitReference){
        this.gitRepoUrl = gitRepoUrl
        this.gitReference = gitReference
    }

    void configure(helper, binding) {
        // N/A
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.gitRepoUrl.first(), notNullValue())
        assertThat(call.args.gitReference.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.gitRepoUrl.first().toString().equals(this.gitRepoUrl)
                && call.args.gitReference.first().toString().equals(this.gitReference)
    }

    String libFunctionName() {
        return 'runGradleCheck'
    }
}
