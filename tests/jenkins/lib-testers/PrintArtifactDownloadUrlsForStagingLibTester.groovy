import static org.hamcrest.MatcherAssert.assertThat
import static org.hamcrest.MatcherAssert.assertThat
import static org.hamcrest.core.IsNull.notNullValue
import static org.hamcrest.core.IsNull.notNullValue

class PrintArtifactDownloadUrlsForStagingLibTester extends LibFunctionTester {

    private List artifactFileNames
    private String uploadPath

    public PrintArtifactDownloadUrlsForStagingLibTester(artifactFileNames, uploadPath){
        this.artifactFileNames = artifactFileNames
        this.uploadPath = uploadPath
    }

    void configure(helper, bindings) {}

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.artifactFileNames.first(), notNullValue())
        assertThat(call.args.uploadPath.first(), notNullValue())
        assert call.args.artifactFileNames.size() > 0
    }

    boolean expectedParametersMatcher(call) {
        return call.args.uploadPath.first().toString().equals(this.uploadPath)
                && call.args.artifactFileNames.first().sort() == this.artifactFileNames.sort()
    }

    String libFunctionName() {
        return 'printArtifactDownloadUrlsForStaging'
    }
}
