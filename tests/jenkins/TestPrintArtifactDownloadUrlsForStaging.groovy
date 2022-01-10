/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*


class TestPrintArtifactDownloadUrlsForStaging extends BuildPipelineTest {

    @Before
    void setUp() {
        super.setUp()
        binding.setVariable('filenamesForUrls', ['dummy_file.tar.gz', 'dummy_file.tar.gz.sig'])
        binding.setVariable('UPLOAD_PATH', 'dummy/upload/path')
    }

    @Test
    void testPrintArtifactDownloadUrlsForStaging() {
        super.testPipeline("tests/jenkins/jobs/PrintArtifactDownloadUrlsForStaging_Jenkinsfile")
    }

}
