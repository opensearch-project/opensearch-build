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
        binding.setVariable('DISTRIBUTION', "docker tar rpm yum deb zip")
        binding.setVariable('ARCHITECTURE', "x64 arm64")
        binding.setVariable('PLATFORM', "linux windows")
        binding.setVariable('PROJECTS', "Both")
        binding.setVariable('ARTIFACT_TYPE', "production")
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
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution docker --arch x64 --os_build_number 6039 --osd_build_number 4104 --projects opensearch opensearch-dashboards --docker_args using-staging-artifact-only --docker_source dockerhub'))
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution tar --arch arm64 --platform linux --os_build_number 6039 --osd_build_number 4104 --projects opensearch opensearch-dashboards --artifact_type production --allow_http false'))
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution rpm --arch x64 --platform linux --os_build_number 6039 --osd_build_number 4104 --projects opensearch opensearch-dashboards --artifact_type production --allow_http false'))
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution yum --arch arm64 --platform linux --os_build_number 6039 --osd_build_number 4104 --projects opensearch opensearch-dashboards --artifact_type production --allow_http false'))
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution deb --arch arm64 --platform linux --os_build_number 6039 --osd_build_number 4104 --projects opensearch opensearch-dashboards --artifact_type production --allow_http false'))
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --version 2.3.0 --distribution zip --arch x64 --platform windows --os_build_number 6039 --osd_build_number 4104 --projects opensearch opensearch-dashboards --artifact_type production --allow_http false'))
    }

    @Test
    public void testFilePath() {
        binding.setVariable('VERSION', "")
        binding.setVariable('OPENSEARCH_ARTIFACT_URL', "https://ci.opensearch/distribution-build-opensearch/1.3.12/8230/linux/x64/tar/opensearch-1.3.12-linux-x64.tar.gz")
        binding.setVariable('OPENSEARCH_DASHBOARDS_ARTIFACT_URL', "https://ci.opensearch/distribution-build-opensearch-dashboards/1.3.12/8230/linux/x64/tar/opensearch-dashboards-1.3.12-linux-x64.tar.gz")
        runScript('jenkins/validate-artifacts/validate-artifacts.jenkinsfile')
        assertThat(getCommandExecutions('sh', 'validation.sh'), hasItem('/tmp/workspace/validation.sh  --file_path opensearch=https://ci.opensearch/distribution-build-opensearch/1.3.12/8230/linux/x64/tar/opensearch-1.3.12-linux-x64.tar.gz opensearch-dashboards=https://ci.opensearch/distribution-build-opensearch-dashboards/1.3.12/8230/linux/x64/tar/opensearch-dashboards-1.3.12-linux-x64.tar.gz --allow_http false'))
    }

    @Test
    public void testWhenFilePathOrVersionNotProvided() {
        binding.setVariable('VERSION', "")
        binding.setVariable('OPENSEARCH_ARTIFACT_URL', "")
        binding.setVariable('OPENSEARCH_DASHBOARDS_ARTIFACT_URL', "")
        runScript('jenkins/validate-artifacts/validate-artifacts.jenkinsfile')
        assertThat(getCommandExecutions('error', ''), hasItem('Both VERSION and OPENSEARCH_ARTIFACT_URL cannot be empty. Please provide either value'))
    }

    @Test
    public void testWhenOSArtifactIsNotProvided() {
        binding.setVariable('OPENSEARCH_ARTIFACT_URL', "")
        binding.setVariable('OPENSEARCH_DASHBOARDS_ARTIFACT_URL', "https://ci.opensearch/distribution-build-opensearch-dashboards/1.3.12/8230/linux/x64/tar/opensearch-dashboards-1.3.12-linux-x64.tar.gz")
        runScript('jenkins/validate-artifacts/validate-artifacts.jenkinsfile')
        assertThat(getCommandExecutions('error', ''), hasItem('Provide OPENSEARCH_ARTIFACT_URL to validate'))
    }

    @Test
    public void testZipArm64IsValidated() {
        runScript('jenkins/validate-artifacts/validate-artifacts.jenkinsfile')
        assertThat(getCommandExecutions('echo', ''), hasItem('Skipping the stage for zip distribution and arm64 architecture'))
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
