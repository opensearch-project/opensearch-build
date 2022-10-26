/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.CoreMatchers.hasItems
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestDockerBuild extends BuildPipelineTest {

    // Variables
    String dockerBuildGitRespository = 'https://github.com/opensearch-project/opensearch-build'
    String dockerBuildGitRespositoryReference = 'main'
    String dockerBuildScriptwithCommands = 'bash docker/ci/build-image-multi-arch.sh -v <TAG_NAME> -f <DOCKERFILE PATH>'

    @Override
    @Before
    void setUp() {

        super.setUp()

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

        // Ensure the entire docker commanbd is executed in an external shell script exactelly once
        def dockerLoginCommand = getCommands('docker').findAll {
            shCommand -> shCommand.contains('docker logout && echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin && eval $DOCKER_BUILD_SCRIPT_WITH_COMMANDS')
        }
        assertThat(dockerLoginCommand.size(), equalTo(1))
        
        // Validate the docker-build.sh is called with correct predefined credential
        assertCallStack().contains("docker-build.sh(echo Account: jenkins-staging-dockerhub-credential)")

        printCallStack()
    }

    def getCommands(String commandString) {
        def shCurlCommands = helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.collect { call ->
            callArgsToString(call)
        }.findAll { externalCommand ->
            externalCommand.contains(commandString)
        }

        return shCurlCommands
    }
    
}
