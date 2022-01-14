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

    @Before
    void setUp() {
        super.setUp()
    }

    @Test
    void testPrintArtifactDownloadUrlsForStaging() {
        def filenamesForUrls = ['dummy_file.tar.gz', 'dummy_file.tar.gz.sig', 'a_dummy_file.tar.gz']
        def uploadPath = 'dummy/upload/path'
        binding.setVariable('filenamesForUrls', filenamesForUrls)
        binding.setVariable('UPLOAD_PATH', uploadPath)

        super.testPipeline("tests/jenkins/jobs/PrintArtifactDownloadUrlsForStaging_Jenkinsfile")

        verifyPrintArtifactDownloadUrlsForStagingParams(helper, filenamesForUrls, uploadPath)
    }

    static void verifyPrintArtifactDownloadUrlsForStagingParams(helper, artifactFileNames, uploadPath) {
        assert helper.callStack.findAll { call ->
            call.methodName == 'printArtifactDownloadUrlsForStaging'
        }.size() > 0

        helper.callStack.findAll { call ->
            call.methodName == 'printArtifactDownloadUrlsForStaging'
        }.each { call ->
            assertThat(call.args.artifactFileNames, notNullValue())
            assertThat(call.args.uploadPath, notNullValue())
            assert call.args.artifactFileNames.size() > 0
            assert call.args.artifactFileNames.first().sort() == artifactFileNames.sort()
            assert call.args.uploadPath.first() == uploadPath
        }
    }

}
