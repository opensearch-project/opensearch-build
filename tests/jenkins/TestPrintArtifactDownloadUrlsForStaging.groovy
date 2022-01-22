/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import jenkins.tests.BuildPipelineTest
import org.junit.*

import static org.hamcrest.MatcherAssert.assertThat
import static org.hamcrest.core.IsNull.notNullValue


class TestPrintArtifactDownloadUrlsForStaging extends BuildPipelineTest {

    private List artifactFileNames
    private String uploadPath

    public LibTester libTester = new LibTester()

    @Before
    void setUp() {

        this.registerLibTester(new TestPrintArtifactDownloadUrlsForStaging(
                artifactFileNames: ['dummy_file.tar.gz', 'dummy_file.tar.gz.sig', 'a_dummy_file.tar.gz'],
                uploadPath: 'dummy/upload/path'
        ).libTester)

        super.setUp()
    }

    @Test
    void testPrintArtifactDownloadUrlsForStaging() {
        super.testPipeline("tests/jenkins/jobs/PrintArtifactDownloadUrlsForStaging_Jenkinsfile")
    }

    class LibTester extends LibFunctionTester {

        void configure(helper, bindings) {}

        void parameterInvariantsAssertions(call) {
            assertThat(call.args.artifactFileNames.first(), notNullValue())
            assertThat(call.args.uploadPath.first(), notNullValue())
            assert call.args.artifactFileNames.size() > 0
        }

        boolean expectedParametersMatcher(call) {
            return call.args.uploadPath.first() == this.uploadPath
                    && call.args.artifactFileNames.first().sort() == this.artifactFileNames.sort()
        }

        String libFunctionName() {
            return 'printArtifactDownloadUrlsForStaging'
        }
    }
}
