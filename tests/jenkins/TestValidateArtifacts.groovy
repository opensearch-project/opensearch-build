/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat
import static org.junit.jupiter.api.Assertions.assertThrows

class TestValidateArtifacts extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('4.2.2')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()

        binding.setVariable('BUILD_NUMBER', '123')

        binding.setVariable('VERSION', "2.3.0")
        binding.setVariable('OS_BUILD_NUMBER', "6039")
        binding.setVariable('OSD_BUILD_NUMBER', "4104")
        binding.setVariable('DISTRIBUTION', "docker tar rpm yum")
        binding.setVariable('ARCHITECTURE', "x64 arm64")
        binding.setVariable('OPTIONAL_ARGS', "using-staging-artifact-only")

        helper.registerAllowedMethod('fileExists', [String.class], { args ->
            return true;
        })
        helper.registerAllowedMethod('unstash', [String.class], null)

    }

    @Test
    public void testValidateArtifactsPipeline() {
        super.testPipeline("jenkins/validate-artifacts/validate-artifacts.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/validate-artifacts/validate-artifacts.jenkinsfile")
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution docker --arch x64 --os-build-number 6039 --osd-build-number 4104 --using-staging-artifact-only '))
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution tar --arch arm64'))
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution rpm --arch x64'))
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution yum --arch arm64'))

    }

    @Test
    public void testDockerArgs() {
        binding.setVariable('OS_BUILD_NUMBER', "")
        binding.setVariable('OSD_BUILD_NUMBER', "")
        runScript('jenkins/validate-artifacts/validate-artifacts.jenkinsfile')
        assertJobStatusFailure()
        assertThat(getCommandExecutions('error', ''), hasItem('Provide OS_BUILD_NUMBER and OSD_BUILD_NUMBER args for Docker Validation'))
    }

    def getCommandExecutions(methodName, command) {
        def shCommands = helper.callStack.findAll {
            call ->
                call.methodName == methodName
        }.
        collect {
            call ->
                callArgsToString(call)
        }.findAll {
            shCommand ->
                shCommand.contains(command)
        }

        return shCommands
    }
}
