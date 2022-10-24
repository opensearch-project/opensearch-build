/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.assertj.core.api.Assertions.assertThat

class TestDockerBuild extends BuildPipelineTest {

    String dockerBuildGitRespository = 'https://github.com/opensearch-project/opensearch-build'
    String dockerBuildGitRespositoryReference = 'main'
    String dockerBuildScriptwithCommands = 'bash docker/ci/build-image-multi-arch.sh -v <TAG_NAME> -f <DOCKERFILE PATH>'

    @Override
    @Before
    void setUp() {

        super.setUp()

        // Variables
        binding.setVariable('DOCKER_BUILD_GIT_REPOSITORY', dockerBuildGitRespository)
        binding.setVariable('DOCKER_BUILD_GIT_REPOSITORY_REFERENCE', dockerBuildGitRespositoryReference)
        binding.setVariable('DOCKER_BUILD_SCRIPT_WITH_COMMANDS', dockerBuildScriptwithCommands)

    }

    @Test
    void DockerBuildRegression() {
        super.testPipeline('jenkins/docker/docker-build.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/docker/docker-build.jenkinsfile')
    }

    @Test
    public void DockerBuildExecuteWithoutErrors() {
        runScript("jenkins/docker/docker-build.jenkinsfile")

        assertJobStatusSuccess()

        assertThat(helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.any { call ->
            callArgsToString(call).contains('docker login')
        }).isTrue()
    }
}
