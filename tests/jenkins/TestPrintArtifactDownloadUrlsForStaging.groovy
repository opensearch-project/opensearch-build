/*
 * Copyright OpenSearch Contributors
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

        this.registerLibTester(new PrintArtifactDownloadUrlsForStagingLibTester(
                ['dummy_file.tar.gz', 'dummy_file.tar.gz.sig', 'a_dummy_file.tar.gz'],
                'dummy/upload/path'
        ))

        super.setUp()
    }

    @Test
    void testPrintArtifactDownloadUrlsForStaging() {
        super.testPipeline("tests/jenkins/jobs/PrintArtifactDownloadUrlsForStaging_Jenkinsfile")
    }
}
