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
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestDockerBuild extends BuildPipelineTest {

    // Variables
    String dockerBuildGitRespository = 'https://github.com/opensearch-project/opensearch-build'
    String dockerBuildGitRespositoryReference = 'main'
    String dockerBuildScriptwithCommands = 'bash docker/ci/build-image-multi-arch.sh -v <TAG_NAME> -f <DOCKERFILE PATH>'
    String dockerBuildOS = 'linux'

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.0.4')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()

        binding.setVariable('DOCKER_BUILD_GIT_REPOSITORY', dockerBuildGitRespository)
        binding.setVariable('DOCKER_BUILD_GIT_REPOSITORY_REFERENCE', dockerBuildGitRespositoryReference)
        binding.setVariable('DOCKER_BUILD_SCRIPT_WITH_COMMANDS', dockerBuildScriptwithCommands)
        binding.setVariable('DOCKER_BUILD_OS', dockerBuildOS)

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

        // Ensure the entire docker command is executed in an external shell script exactly once
        def dockerLoginCommand = getCommands('docker').findAll {
            shCommand -> shCommand.contains('docker logout && echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin && eval $DOCKER_BUILD_SCRIPT_WITH_COMMANDS')
        }
        assertThat(dockerLoginCommand.size(), equalTo(1))

        // Validate the docker-build.sh is called with correct predefined credential
        assertCallStack().contains("docker-build.sh(echo Account: jenkins-staging-dockerhub-credential)")

        // Make sure dockerBuildOS is deciding agent_node docker_nodes docker_args correctly
        assertCallStack().contains("docker-build.echo(Executing on agent [docker:[alwaysPull:true, args:-u root -v /var/run/docker.sock:/var/run/docker.sock, containerPerStageRoot:false, label:Jenkins-Agent-Ubuntu2004-X64-M52xlarge-Docker-Builder, image:opensearchstaging/ci-runner:ubuntu2004-x64-docker-buildx0.9.1-qemu5.0-v1, reuseNode:false, registryUrl:https://public.ecr.aws/, stages:[:]]])")

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
