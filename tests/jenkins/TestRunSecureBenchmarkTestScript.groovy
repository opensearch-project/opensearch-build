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

class TestRunSecureBenchmarkTestScript extends BuildPipelineTest{
    @Override
    @Before
    void setUp() {
        helper.registerSharedLibrary(
                library().name('jenkins')
                        .defaultVersion('5.7.0')
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
        helper.registerAllowedMethod("downloadBuildManifest", [Map], {
            c -> lib.jenkins.BuildManifest.new(readYaml(file: 'tests/jenkins/data/opensearch-1.3.0-bundle.yml'))
        })
        helper.registerAllowedMethod('parameterizedCron', [String], null)
        helper.registerAllowedMethod("cfnDescribe", [Map])
        helper.registerAllowedMethod("cfnDelete", [Map])
        binding.setVariable('AGENT_LABEL', 'Jenkins-Agent-AL2-X64-M52xlarge-Docker-Host-Benchmark-Test')
        binding.setVariable('ARCHITECTURE', 'x64')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'test_bucket')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('env', ['BUILD_NUMBER': '307'])
        binding.setVariable('BUILD_NUMBER', '307')
        binding.setVariable('BUILD_URL', 'test://artifact.url')
        binding.setVariable('BUILD_ID', '1234')
        binding.setVariable('BUNDLE_MANIFEST', 'tests/jenkins/data/opensearch-1.3.0-bundle.yml')
        binding.setVariable('BUNDLE_MANIFEST_URL', 'test://artifact.url')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'bot_token_name')
        binding.setVariable('GITHUB_USER', 'test_user')
        binding.setVariable('GITHUB_TOKEN', 'test_token')
        binding.setVariable('HAS_SECURITY', 'true')
        binding.setVariable('SINGLE_NODE_CLUSTER', 'false')
        binding.setVariable('MIN_DISTRIBUTION', 'false')
        binding.setVariable('USE_50_PERCENT_HEAP', 'true')
        binding.setVariable('ENABLE_REMOTE_STORE', 'true')
        binding.setVariable('SUFFIX', '1234')
        binding.setVariable('MANAGER_NODE_COUNT', '3')
        binding.setVariable('DATA_NODE_COUNT', '3')
        binding.setVariable('USER_TAGS', 'run-type:test')
        binding.setVariable('WORKLOAD_PARAMS', '')
        binding.setVariable('ADDITIONAL_CONFIG', '')
        binding.setVariable('CLIENT_NODE_COUNT', '')
        binding.setVariable('INGEST_NODE_COUNT', '')
        binding.setVariable('ML_NODE_COUNT', '')
        binding.setVariable('DATA_NODE_STORAGE', '100')
        binding.setVariable('ML_NODE_STORAGE', '')
        binding.setVariable('DATA_INSTANCE_TYPE', '')
        binding.setVariable('JVM_SYS_PROPS', '')
        binding.setVariable('CAPTURE_NODE_STAT', 'false')
        binding.setVariable('CAPTURE_SEGMENT_REPLICATION_STAT', 'true')
        binding.setVariable('JOB_NAME', 'benchmark-test')
        binding.setVariable('BENCHMARK_TEST_CONFIG_LOCATION', 'test_config')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'test://artifact.url')
        binding.setVariable('STAGE_NAME', 'test_stage')
        binding.setVariable('TEST_WORKLOAD', 'nyc-taxis')
        binding.setVariable('WEBHOOK_URL', 'test://artifact.url')
        binding.setVariable('TELEMETRY_PARAMS', '{"telemetry_setting":"value"}')

        super.setUp()
    }

    @Test
    public void testRunSecureBenchmarkTestScript_verifyPipeline() {
        super.testPipeline("jenkins/opensearch/benchmark-test.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/opensearch/secure-benchmark-test.jenkinsfile")
    }

    @Test
    void testRunSecureBenchmarkTestScript_verifyArtifactDownloads() {
        runScript("jenkins/opensearch/benchmark-test.jenkinsfile")

        def curlCommands = getCommandExecutions('sh', 'curl').findAll {
            shCommand -> shCommand.contains('curl')
        }

        assertThat(curlCommands.size(), equalTo(4))
        assertThat(curlCommands, hasItem(
                "curl -sSL test://artifact.url --output tests/jenkins/data/opensearch-1.3.0-bundle.yml".toString()
        ))

        def s3DownloadCommands = getCommandExecutions('s3Download', 'bucket').findAll {
            shCommand -> shCommand.contains('bucket')
        }

        assertThat(s3DownloadCommands.size(), equalTo(4))
        assertThat(s3DownloadCommands, hasItems(
                "{file=config.yml, bucket=ARTIFACT_BUCKET_NAME, path=test_config/config.yml, force=true}".toString(),
                "{file=benchmark.ini, bucket=ARTIFACT_BUCKET_NAME, path=test_config/benchmark.ini, force=true}".toString()
        ))
    }


    @Test
    void testRunSecureBenchmarkTestScript_verifyScriptExecutions() {
        runScript("jenkins/opensearch/benchmark-test.jenkinsfile")

        def testScriptCommands = getCommandExecutions('sh', './test.sh').findAll {
            shCommand -> shCommand.contains('./test.sh')
        }

        assertThat(testScriptCommands.size(), equalTo(2))
        assertThat(testScriptCommands, hasItems(
                "./test.sh benchmark-test --bundle-manifest tests/jenkins/data/opensearch-1.3.0-bundle.yml --config /tmp/workspace/config.yml --workload nyc-taxis --benchmark-config /tmp/workspace/benchmark.ini --user-tag distribution-build-id:1236,arch:x64,os-commit-id:22408088f002a4fc8cdd3b2ed7438866c14c5069,run-type:test,security-enabled:true    --use-50-percent-heap --enable-remote-store  --capture-segment-replication-stat --suffix 307-secure --manager-node-count 3 --data-node-count 3       --data-node-storage 100   --telemetry-params '{\"telemetry_setting\":\"value\"}'".toString(),
                "./test.sh benchmark-test --bundle-manifest tests/jenkins/data/opensearch-1.3.0-bundle.yml --config /tmp/workspace/config.yml --workload nyc-taxis --benchmark-config /tmp/workspace/benchmark.ini --user-tag distribution-build-id:1236,arch:x64,os-commit-id:22408088f002a4fc8cdd3b2ed7438866c14c5069,run-type:test,security-enabled:false --without-security   --use-50-percent-heap --enable-remote-store  --capture-segment-replication-stat --suffix 307 --manager-node-count 3 --data-node-count 3       --data-node-storage 100   --telemetry-params '{\"telemetry_setting\":\"value\"}'".toString()
        ))
    }

    @Test
    void testRunNonSecurityBenchmarkTestScript_verifyJob_aborted() throws Exception{
        binding.setVariable('BUNDLE_MANIFEST', 'tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml')
        binding.setVariable('HAS_SECURITY', false)
        helper.registerAllowedMethod("cfnDescribe", [Map.class]) { args -> return true}
        helper.registerAllowedMethod('sh', [String.class], { String cmd ->
            updateBuildStatus('ABORTED')
        })
        runScript("jenkins/opensearch/benchmark-test.jenkinsfile")

        assertJobStatusAborted()
        assertCallStack()
        assertCallStack().contains("cfnDescribe({stack=opensearch-infra-stack-307-1234-x64})")
        assertCallStack().contains("cfnDelete({stack=opensearch-infra-stack-307-1234-x64, pollInterval=1000})")
        assertCallStack().contains("cfnDescribe({stack=opensearch-infra-stack-307-secure-1234-x64})")
        assertCallStack().contains("cfnDelete({stack=opensearch-infra-stack-307-secure-1234-x64, pollInterval=1000})")
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
