import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class GetRepositoryCommitLibTester extends LibFunctionTester {

    private String componentName
    private String inputManifest
    private String outputFile

    public GetRepositoryCommitLibTester(componentName, inputManifest, outputFile){
        this.componentName = componentName
        this.inputManifest = inputManifest
        this.outputFile = outputFile
    }

    void configure(helper, binding) {
        // N/A
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.inputManifest.first(), notNullValue())
        assertThat(call.args.outputFile.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.inputManifest.first().toString().equals(this.inputManifest)
                && call.args.outputFile.first().toString().equals(this.outputFile)
    }

    String libFunctionName() {
        return 'getRepositoryCommit'
    }
}
