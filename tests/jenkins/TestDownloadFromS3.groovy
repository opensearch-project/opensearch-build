/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test


class TestDownloadFromS3 extends BuildPipelineTest {

    @Before
    void setUp() {

        this.registerLibTester(new DownloadFromS3LibTester('/tmp/src/path' , 'dummy_bucket', '/download/path', true))

        super.setUp()
    }

    @Test
    public void testDownloadFromS3() {
        super.testPipeline("tests/jenkins/jobs/DownloadFromS3_Jenkinsfile")
    }
}
