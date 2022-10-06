/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestDockerScanJob extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        super.setUp()

        // Variables
        binding.setVariable('IMAGE_FULL_NAME', 'alpine:3')

    }

    @Test
    void DockerScan_test() {
        super.testPipeline('jenkins/docker/docker-scan.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/docker/docker-scan.jenkinsfile')
    }
}
