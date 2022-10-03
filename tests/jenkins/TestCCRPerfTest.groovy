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

import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat

import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestCCRPerfTest extends BuildPipelineTest {

    @Override   
    @Before
    void setUp() {

        super.setUp()

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.0.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
        )

        binding.setVariable('AGENT_LABEL', 'Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host')
        binding.setVariable('AGENT_IMAGE', 'opensearchstaging/ci-runner:ci-runner-centos7-v1')
        binding.setVariable('ARCHITECTURE', 'x64')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'test_bucket')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('BUILD_ID', '1236')
        binding.setVariable('env', ['BUILD_NUMBER': '307'])
        binding.setVariable('BUILD_NUMBER', '307')
        binding.setVariable('BUILD_URL', 'test://artifact.url')
        binding.setVariable('BUNDLE_MANIFEST', 'tests/jenkins/data/opensearch-1.3.0-bundle.yml')
        binding.setVariable('BUNDLE_MANIFEST_URL', 'test://artifact.url')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'bot_token_name')
        binding.setVariable('GITHUB_USER', 'test_user')
        binding.setVariable('GITHUB_TOKEN', 'test_token')
        binding.setVariable('HAS_SECURITY', true)
        binding.setVariable('JOB_NAME', 'perf-test')
        binding.setVariable('PERF_TEST_CONFIG_LOCATION', 'test_config')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'test://artifact.url')
        binding.setVariable('STAGE_NAME', 'test_stage')
        binding.setVariable('TEST_ITERATIONS', '1')
        binding.setVariable('TEST_WORKLOAD', 'nyc_taxis')
        binding.setVariable('WEBHOOK_URL', 'test://artifact.url')
        binding.setVariable('WARMUP_ITERATIONS', '1')
        
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("uploadTestResults", [Map])
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], {
            args,
            closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('findFiles', [Map.class], null)
        helper.registerAllowedMethod("withCredentials", [Map])
        helper.registerAllowedMethod("downloadBuildManifest", [Map], {
            c -> lib.jenkins.BuildManifest.new(readYaml(file: 'tests/jenkins/data/opensearch-1.3.0-bundle.yml'))
        })
        helper.registerAllowedMethod('parameterizedCron', [String], null)
    }

    @Test
    public void testCCRPerfTestScript_Pipeline() {
        super.testPipeline("jenkins/cross-cluster-replication/perf-test.jenkinsfile",
        "tests/jenkins/jenkinsjob-regression-files/cross-cluster-replication/perf-test.jenkinsfile")
    }

    @Test
    void testCCRestScript_verifyArtifactDownloads() {
        runScript("jenkins/cross-cluster-replication/perf-test.jenkinsfile")

        def curlCommands = getCommandExecutions('sh', 'curl').findAll {
            shCommand -> shCommand.contains('curl')
        }

        assertThat(curlCommands.size(), equalTo(3))

        def s3DownloadCommands = getCommandExecutions('s3Download', 'bucket').findAll {
            shCommand -> shCommand.contains('bucket')
        }

        assertThat(s3DownloadCommands.size(), equalTo(1))
        assertThat(s3DownloadCommands, hasItem(
            "{file=config.yml, bucket=ARTIFACT_BUCKET_NAME, path=test_config/config-ccr.yml, force=true}".toString()
        ))
    }

    @Test
    void testCCRPerfTestScript_verifyPackageInstallation() {
        runScript("jenkins/cross-cluster-replication/perf-test.jenkinsfile")

        def pipenvCommands = getCommandExecutions('sh', 'pipenv').findAll {
            shCommand -> shCommand.contains('pipenv')
        }

        assertThat(pipenvCommands.size(), equalTo(1))

    }

    @Test
    void testCCRPerfTestScript_verifyScriptExecutions() {
        runScript("jenkins/cross-cluster-replication/perf-test.jenkinsfile")

        def testScriptCommands = getCommandExecutions('sh', './test.sh').findAll {
            shCommand -> shCommand.contains('./test.sh')
        }

        assertThat(testScriptCommands.size(), equalTo(1))
        assertThat(testScriptCommands, hasItem(
            "./test.sh perf-test --stack test-single-security-1236-x64-perf-test --bundle-manifest tests/jenkins/data/opensearch-1.3.0-bundle.yml --config config.yml     --component cross-cluster-replication".toString()
        ))

        def resultUploadScriptCommands = getCommandExecutions('s3Upload', 'test-results').findAll {
            shCommand -> shCommand.contains('test-results')
        }
        assertThat(resultUploadScriptCommands.size(), equalTo(1))
        assertThat(resultUploadScriptCommands, hasItem(
            "{file=test-results, bucket=ARTIFACT_BUCKET_NAME, path=perf-test/1.3.0/1236/linux/x64/tar/test-results/1236}".toString()
        ))
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
