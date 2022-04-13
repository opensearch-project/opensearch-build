import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class UploadIndexFileLibTester extends LibFunctionTester {

    private String indexFilePath

    public UploadIndexFileLibTester(indexFilePath) {
        this.indexFilePath = indexFilePath
    }

    void configure(helper, binding) {
        binding.setVariable('BUILD_NUMBER', '123')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'dummy_bucket_name')

        helper.registerAllowedMethod("writeJSON", [Map])
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.indexFilePath.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.indexFilePath.first().toString().equals(this.indexFilePath)
    }

    String libFunctionName() {
        return 'uploadIndexFile'
    }

}
