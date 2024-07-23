/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml

import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat

import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestReleaseBranch extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('6.3.3')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()

        def manifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.0/latest/linux/x64/tar/builds/opensearch/manifest.yml"
        def buildManifest = "tests/jenkins/data/opensearch-1.3.0-build.yml"

        binding.setVariable('MANIFEST_FILE', manifestUrl)
        binding.setVariable('SOURCE_BRANCH', "2.x")
        binding.setVariable('TARGET_BRANCH', "2.11")


        binding.setVariable('BUILD_MANIFEST', buildManifest)

        helper.registerAllowedMethod("withCredentials", [Map])
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((buildManifest as File).text)
        })

        helper.addShMock("""git ls-remote https://github.com/opensearch-project/OpenSearch.git 2.11""") { script ->
            return [stdout: "", exitValue: 0]
        }

    }

    @Test
    public void testBranchCreation() {
        super.testPipeline('jenkins/release-workflows/release-branch.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/release-branch-buildmanifest.jenkinsfile')
    }

    @Test
    public void testBranchExistence() {
        helper.addShMock("""git ls-remote https://github.com/opensearch-project/OpenSearch.git 2.11""") { script ->
            return [stdout: "ref/2.11", exitValue: 0]
        }
        runScript('jenkins/release-workflows/release-branch.jenkinsfile')
        assertThat(getCommandExecutions('echo', ''), hasItem('Branch already exists, skipping branch creation for the repo https://github.com/opensearch-project/OpenSearch.git'))
    }

    @Test
    public void testInputManifest() {
        binding.setVariable('MANIFEST_FILE', "2.0.0/opensearch-2.0.0.yml")
        def inputManifest = "tests/jenkins/data/opensearch-2.0.0.yml"
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((inputManifest as File).text)
        })
        helper.addShMock("""git ls-remote https://github.com/opensearch-project/OpenSearch.git 2.11""") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("""git ls-remote https://github.com/opensearch-project/common-utils.git 2.11""") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("""git ls-remote https://github.com/opensearch-project/job-scheduler.git 2.11""") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("""git ls-remote https://github.com/opensearch-project/OpenSearch.git 2.11""") { script ->
            return [stdout: "", exitValue: 0]
        }

        super.testPipeline('jenkins/release-workflows/release-branch.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/release-branch-inputmanifest.jenkinsfile')
    }

    @Test
    public void testVerifyParameters() {
        binding.setVariable('MANIFEST_FILE', "")
        binding.setVariable('TARGET_BRANCH', "")
        runScript('jenkins/release-workflows/release-branch.jenkinsfile')
        assertThat(getCommandExecutions('error', ''), hasItem('Required parameters are missing. Please provide the mandatory arguments MANIFEST_FILE, SOURCE_BRANCH and TARGET_BRANCH'))
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
