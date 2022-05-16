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
                'public.ecr.aws/opensearchproject/ci-runner:latest',
                'ecr',
                'public.ecr.aws/opensearchproject',
                true))

        this.registerLibTester(new CopyContainerLibTester('opensearchstaging/ci-runner:latest',
                'public.ecr.aws/opensearchstaging/ci-runner:latest',
                'ecr',
                'public.ecr.aws/opensearchstaging',
                false))

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
