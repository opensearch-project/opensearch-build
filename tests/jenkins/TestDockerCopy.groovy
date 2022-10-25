/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.assertj.core.api.Assertions.assertThat

class TestDockerCopy extends BuildPipelineTest {

    String sourceImageRegistry = 'opensearchstaging'
    String sourceImage = 'opensearch:1.3.2'
    String destinationImageRegistry = 'opensearchproject'
    String destinationImage = 'opensearch:1.3.2'

    @Override
    @Before
    void setUp() {

        super.setUp()

        // Variables
        binding.setVariable('SOURCE_IMAGE_REGISTRY', sourceImageRegistry)
        binding.setVariable('SOURCE_IMAGE', sourceImage)
        binding.setVariable('DESTINATION_IMAGE_REGISTRY', destinationImageRegistry)
        binding.setVariable('DESTINATION_IMAGE', destinationImage)

    }

    @Test
    void DockerCopyRegression() {
        super.testPipeline('jenkins/docker/docker-copy.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/docker/docker-copy.jenkinsfile')
    }

    @Test
    public void DockerCopyExecuteWithoutErrors() {
        runScript("jenkins/docker/docker-copy.jenkinsfile")

        assertJobStatusSuccess()

        // Ensure 'docker login' is executed in an external shell script
        assertThat(helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.any { call ->
            callArgsToString(call).contains('docker login')
        }).isTrue()

        // Validate the copyContainer docker-copy.sh is called
        assertCallStack().contains("docker-copy.copyContainer")

        printCallStack()
    }
}