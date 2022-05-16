/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.*


class TestCopyDockerECRContainer extends BuildPipelineTest {

    @Before
    void setUp() {

        this.registerLibTester(new CopyDockerContainerLibTester('opensearchstaging/ci-runner', '2.0.0', true, true, true))

        this.registerLibTester(new CopyECRContainerLibTester('opensearchstaging/ci-runner', '2.0.0', true, true, true))

        super.setUp()
    }

    @Test
    public void testForDockerhubECR() {
        super.testPipeline("tests/jenkins/jobs/CopyContainer_docker_Jenkinsfile")
    }
}
