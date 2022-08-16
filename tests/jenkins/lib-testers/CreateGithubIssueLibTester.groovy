import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.CoreMatchers.nullValue
import static org.hamcrest.MatcherAssert.assertThat

class CreateGithubIssueLibTester extends LibFunctionTester{
    private List<String> message

    public CreateGithubIssueLibTester(message){
        this.message = message
    }

    @Override
    String libFunctionName() {
        return 'createGithubIssue'
    }

    @Override
    void parameterInvariantsAssertions(Object call) {
        assertThat(call.args.message.first(), notNullValue())
    }

    @Override
    boolean expectedParametersMatcher(Object call) {
        //return false
        return call.args.message.first().equals(this.message)
    }

    @Override
    void configure(Object helper, Object binding) {
        helper.registerAllowedMethod("withCredentials", [Map])
        helper.registerAllowedMethod("sleep", [Map])
        binding.setVariable('BUILD_URL', 'www.example.com/jobs/test/123/')
        binding.setVariable('INPUT_MANIFEST', '2.0.0/opensearch-2.0.0.yml')
    }
}
