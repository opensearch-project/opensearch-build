/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.MatcherAssert.assertThat
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
