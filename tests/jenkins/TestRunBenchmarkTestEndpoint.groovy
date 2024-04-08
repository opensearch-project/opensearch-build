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
import static org.hamcrest.CoreMatchers.hasItems
import static org.hamcrest.MatcherAssert.assertThat

import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestRunBenchmarkTestEndpoint extends BuildPipelineTest{
    @Override
    @Before
    void setUp() {
        helper.registerSharedLibrary(
                library().name('jenkins')
                        .defaultVersion('6.4.1')
                        .allowOverride(true)
                        .implicit(true)
                        .targetPath('vars')
                        .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                        .build()
        )
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
        binding.setVariable('AGENT_LABEL', 'Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host')
        binding.setVariable('AGENT_IMAGE', 'opensearchstaging/ci-runner:ci-runner-centos7-v1')
        binding.setVariable('ARCHITECTURE', 'x64')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'test_bucket')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('CLUSTER_ENDPOINT', 'opensearch-ABCxdfdfhyfk.com')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'bot_token_name')
        binding.setVariable('GITHUB_USER', 'test_user')
        binding.setVariable('GITHUB_TOKEN', 'test_token')
        binding.setVariable('USER_TAGS', 'run-type:test')
        binding.setVariable('WORKLOAD_PARAMS', '')
        binding.setVariable('TEST_PROCEDURE', 'append-no-conflicts')
        binding.setVariable('EXCLUDE_TASKS', '')
        binding.setVariable('INCLUDE_TASKS', '')
        binding.setVariable('ADDITIONAL_CONFIG', '')
        binding.setVariable('BENCHMARK_TEST_CONFIG_LOCATION', 'test_config')
        binding.setVariable('STAGE_NAME', 'test_stage')
        binding.setVariable('TEST_WORKLOAD', 'nyc-taxis')
        binding.setVariable('TELEMETRY_PARAMS', '{"telemetry_setting":"value"}')

        super.setUp()
    }

    @Test
    public void testRunSecureBenchmarkTestScript_verifyPipeline() {
        addParam('SECURITY_ENABLED', true)
        super.testPipeline("jenkins/opensearch/benchmark-test-endpoint.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/opensearch/benchmark-test-endpoint-secure.jenkinsfile")
    }

    @Test
    void testRunSecureBenchmarkTestScript_verifyArtifactDownloads() {
        runScript("jenkins/opensearch/benchmark-test-endpoint.jenkinsfile")

        def curlCommands = getCommandExecutions('sh', 'curl').findAll {
            shCommand -> shCommand.contains('curl')
        }

        def s3DownloadCommands = getCommandExecutions('s3Download', 'bucket').findAll {
            shCommand -> shCommand.contains('bucket')
        }

        assertThat(s3DownloadCommands.size(), equalTo(1))
        assertThat(s3DownloadCommands, hasItems(
                "{file=benchmark.ini, bucket=ARTIFACT_BUCKET_NAME, path=test_config/benchmark.ini, force=true}".toString()
        ))
    }


    @Test
    void testRunSecureBenchmarkTestScript_verifyScriptExecutions() {
        addParam('SECURITY_ENABLED', true)
        runScript("jenkins/opensearch/benchmark-test-endpoint.jenkinsfile")

        def testScriptCommands = getCommandExecutions('sh', './test.sh').findAll {
            shCommand -> shCommand.contains('./test.sh')
        }

        assertThat(testScriptCommands.size(), equalTo(1))
        assertThat(testScriptCommands, hasItems(
                "./test.sh benchmark-test    --cluster-endpoint opensearch-ABCxdfdfhyfk.com  --workload nyc-taxis --benchmark-config /tmp/workspace/benchmark.ini --user-tag run-type:test,security-enabled:true                --test-procedure append-no-conflicts       --telemetry-params '{\"telemetry_setting\":\"value\"}'".toString()
        ))
    }
    @Test
    public void testRunSecureBenchmarkTestWithoutSecurity_verifyPipeline() {
        addParam('SECURITY_ENABLED', true)
        super.testPipeline("jenkins/opensearch/benchmark-test-endpoint.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/opensearch/benchmark-test-endpoint-insecure.jenkinsfile")
    }

    @Test
    void testRunSecureBenchmarkTestScript_verifyWithoutSecurity() {
        addParam('SECURITY_ENABLED', false)
        runScript("jenkins/opensearch/benchmark-test-endpoint.jenkinsfile")

        def testScriptCommands = getCommandExecutions('sh', './test.sh').findAll {
            shCommand -> shCommand.contains('./test.sh')
        }

        assertThat(testScriptCommands.size(), equalTo(1))
        assertThat(testScriptCommands, hasItems(
                "./test.sh benchmark-test    --cluster-endpoint opensearch-ABCxdfdfhyfk.com  --workload nyc-taxis --benchmark-config /tmp/workspace/benchmark.ini --user-tag run-type:test,security-enabled:false --without-security               --test-procedure append-no-conflicts       --telemetry-params '{\"telemetry_setting\":\"value\"}'".toString()
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
