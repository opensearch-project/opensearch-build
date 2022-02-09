/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.*


class TestCopyContainer extends BuildPipelineTest {

    @Before
    void setUp() {

        this.registerLibTester(new CopyContainerLibTester('opensearchstaging/ci-runner:latest',
                'opensearchproject/ci-runner:latest',
                'ecr',
                'public.ecr.aws/p5f6l6i3',
                'DUMMY_ACCOUNT_NAME'))

        this.registerLibTester(new CopyContainerLibTester('opensearchstaging/ci-runner:latest',
                'opensearchproject/ci-runner:latest',
                'docker',
                'jenkins-staging-docker-prod-token'))

        super.setUp()
    }

    @Test
    public void testForDockerhub() {
        super.testPipeline("tests/jenkins/jobs/CopyContainer_docker_Jenkinsfile")
    }
}
