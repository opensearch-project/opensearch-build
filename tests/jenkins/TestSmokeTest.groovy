/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml

import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat

class TestSmokeTest extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('8.1.1')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()

        def jobName = "dummy_job"
        def agentLabel = "Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host"

        binding.setVariable('env', ['BUILD_NUMBER': '234', 'PUBLIC_ARTIFACT_URL': 'DUMMY_PUBLIC_ARTIFACT_URL', 'JOB_NAME': 'dummy_job', 'DOCKER_AGENT':[image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11']])
        binding.setVariable('BUILD_JOB_NAME', 'dummy_job')
        binding.setVariable('AGENT_LABEL', agentLabel)
        binding.setVariable('BUILD_NUMBER', '234')

        helper.registerAllowedMethod('unstash', [String.class], null)
    }

    @Test
    void smokeTests_runs() {
        def buildManifest = "tests/jenkins/data/opensearch-2.19.0-build.yml"
        def testManifest = "tests/jenkins/data/opensearch-2.19.0-test.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.19.0/10545/linux/x64/tar/builds/opensearch/manifest.yml"

        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('TEST_MANIFEST', testManifest)
        helper.addFileExistsMock("manifests/${testManifest}", true)

        helper.registerAllowedMethod("readYaml", [Map.class], { args ->
            if (args.file == 'manifests/tests/jenkins/data/opensearch-2.19.0-test.yml') {
                return new Yaml().load((testManifest as File).text)
            } else if (args.file == 'tests/jenkins/data/opensearch-2.19.0-build.yml') {
                return new Yaml().load((buildManifest as File).text)
            } else {
                println("Manifest not found ${args.file}")
            }
        })

        super.testPipeline('jenkins/opensearch/smoke-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch/smoke-test.jenkinsfile')
        assertThat(getCommandExecutions('sh', 'test.sh'), hasItem(' ./test.sh smoke-test manifests/tests/jenkins/data/opensearch-2.19.0-test.yml --test-run-id 234 --paths opensearch=https://ci.opensearch.org/ci/dbc/dummy_job/2.19.0/10545/linux/x64/tar '))
    }

    @Test
    void smokeTests_runs_rpm() {
        def buildManifest = "tests/jenkins/data/opensearch-2.19.0-build-rpm.yml"
        def testManifest = "tests/jenkins/data/opensearch-2.19.0-test.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.19.0/10691/linux/arm64/rpm/builds/opensearch/manifest.yml"

        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('TEST_MANIFEST', testManifest)
        helper.addFileExistsMock("manifests/${testManifest}", true)

        helper.registerAllowedMethod("readYaml", [Map.class], { args ->
            if (args.file == 'manifests/tests/jenkins/data/opensearch-2.19.0-test.yml') {
                return new Yaml().load((testManifest as File).text)
            } else if (args.file == 'tests/jenkins/data/opensearch-2.19.0-build-rpm.yml') {
                return new Yaml().load((buildManifest as File).text)
            } else {
                println("Manifest not found ${args.file}")
            }
        })

        super.testPipeline('jenkins/opensearch/smoke-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch/smoke-test-rpm.jenkinsfile')
        assertThat(getCommandExecutions('sh', 'test.sh'), hasItem('su `id -un 1000` -c \" ./test.sh smoke-test manifests/tests/jenkins/data/opensearch-2.19.0-test.yml --test-run-id 234 --paths opensearch=https://ci.opensearch.org/ci/dbc/dummy_job/2.19.0/10691/linux/arm64/rpm \"'))
    }

    @Test
    void checkError() {
        def buildManifest = "tests/jenkins/data/opensearch-2.19.0-build.yml"
        def testManifest = "tests/jenkins/data/opensearch-2.19.0-test.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.19.0/10545/linux/x64/tar/builds/opensearch/manifest.yml"

        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('TEST_MANIFEST', testManifest)
        helper.addFileExistsMock("manifests/${testManifest}", true)

        helper.registerAllowedMethod("readYaml", [Map.class], { args ->
            if (args.file == 'manifests/tests/jenkins/data/opensearch-2.19.0-test.yml') {
                return new Yaml().load((testManifest as File).text)
            } else if (args.file == 'tests/jenkins/data/opensearch-2.19.0-build.yml') {
                return new Yaml().load((buildManifest as File).text)
            } else {
                println("Manifest not found ${args.file}")
            }
        })

        helper.addFileExistsMock('manifests/tests/jenkins/data/opensearch-2.19.0-test.yml', false)
        runScript('jenkins/opensearch/smoke-test.jenkinsfile')
        assertThat(getCommandExecutions('error', ''), hasItem('Smoke Tests failed to start. Test manifest was not provided or not found in manifests/tests/jenkins/data/opensearch-2.19.0-test.yml.'))
        assertJobStatusFailure()
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
