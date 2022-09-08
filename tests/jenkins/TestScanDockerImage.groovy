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


class TestScanDockerImage extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new ScanDockerImageLibTester(
            "opensearchstaging/opensearch:2.0.0",
            "scan_docker_image"
            )
        )
        super.setUp()
    }

    @Test
    void testScanDockerImage() {
        super.testPipeline("tests/jenkins/jobs/ScanDockerImage_Jenkinsfile")
    }
}
