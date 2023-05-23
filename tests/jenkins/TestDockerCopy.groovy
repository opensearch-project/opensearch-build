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

class TestDockerCopy extends BuildPipelineTest {

    String sourceImageRegistry = 'opensearchstaging'
    String sourceImage = 'ci-runner:testtag'
    String destinationImageRegistry = 'public.ecr.aws/opensearchstaging'
    String destinationImage = 'ci-runner:testtag2'

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('4.2.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

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

        // Ensure the gcrane is executed in an external shell script exactely once
        def copyContainerCommand = getCommands('crane').findAll {
            shCommand -> shCommand.contains('set -x && crane cp opensearchstaging/ci-runner:testtag public.ecr.aws/opensearchstaging/ci-runner:testtag2')
        }
        assertThat(copyContainerCommand.size(), equalTo(1))

        // Validating docker-copy.jenkinsfile does run copyContainer.groovy 
        assertCallStack().contains("docker-copy.copyContainer")

        printCallStack()
    }

    @Test
    public void DockerCopyExecuteAllTagsWithoutErrors() {
        addParam('ALL_TAGS', true)
        runScript("jenkins/docker/docker-copy.jenkinsfile")

        assertJobStatusSuccess()

        // Ensure the gcrane is executed in an external shell script exactely once
        def copyContainerCommand = getCommands('crane').findAll {
            shCommand -> shCommand.contains('set -x && crane cp opensearchstaging/ci-runner public.ecr.aws/opensearchstaging/ci-runner --all-tags')
        }
        assertThat(copyContainerCommand.size(), equalTo(1))

        // Validating docker-copy.jenkinsfile does run copyContainer.groovy 
        assertCallStack().contains("docker-copy.copyContainer")

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
