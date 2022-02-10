/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.*


class TestSignArtifacts extends BuildPipelineTest {

    @Before
    void setUp() {

        this.registerLibTester(new SignArtifactsLibTester('.sig', 'linux', "${this.workspace}/artifacts", null, null))
        this.registerLibTester(new SignArtifactsLibTester(null, 'linux', "${this.workspace}/file.yml", 'maven', null))
        super.setUp()
    }

    @Test
    void testSignArtifacts() {
        super.testPipeline("tests/jenkins/jobs/SignArtifacts_Jenkinsfile")
    }
}
