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

class TestRunNonSecBenchmarkTestScript extends BuildPipelineTest{
    @Override
    @Before
    void setUp() {
        helper.registerSharedLibrary(
                library().name('jenkins')
                        .defaultVersion('6.8.0')
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
            c -> lib.jenkins.BuildManifest.new(readYaml(file: 'tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml'))
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
        binding.setVariable('BUNDLE_MANIFEST', 'tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml')
        binding.setVariable('BUNDLE_MANIFEST_URL', 'test://artifact.url')
        binding.setVariable('DISTRIBUTION_URL', '')
        binding.setVariable('DISTRIBUTION_VERSION', '')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'bot_token_name')
        binding.setVariable('GITHUB_USER', 'test_user')
        binding.setVariable('GITHUB_TOKEN', 'test_token')
        binding.setVariable('HAS_SECURITY', 'false')
        binding.setVariable('SINGLE_NODE_CLUSTER', 'false')
        binding.setVariable('MIN_DISTRIBUTION', 'false')
        binding.setVariable('USE_50_PERCENT_HEAP', 'true')
        binding.setVariable('SUFFIX', '1234')
        binding.setVariable('MANAGER_NODE_COUNT', '3')
        binding.setVariable('DATA_NODE_COUNT', '3')
        binding.setVariable('ENABLE_REMOTE_STORE', 'false')
        binding.setVariable('USER_TAGS', 'run-type:test')
        binding.setVariable('WORKLOAD_PARAMS', '')
        binding.setVariable('TEST_PROCEDURE', 'append-no-conflicts')
        binding.setVariable('EXCLUDE_TASKS', 'type:search,scroll')
        binding.setVariable('INCLUDE_TASKS', 'type:search,scroll')
        binding.setVariable('ADDITIONAL_CONFIG', '')
        binding.setVariable('CLIENT_NODE_COUNT', '')
        binding.setVariable('INGEST_NODE_COUNT', '')
        binding.setVariable('ML_NODE_COUNT', '')
        binding.setVariable('DATA_NODE_STORAGE', '100')
        binding.setVariable('ML_NODE_STORAGE', '')
        binding.setVariable('DATA_INSTANCE_TYPE', 'r5-4xlarge')
        binding.setVariable('JVM_SYS_PROPS', '')
        binding.setVariable('CAPTURE_NODE_STAT', 'false')
        binding.setVariable('CAPTURE_SEGMENT_REPLICATION_STAT', 'false')
        binding.setVariable('JOB_NAME', 'benchmark-test')
        binding.setVariable('BENCHMARK_TEST_CONFIG_LOCATION', 'test_config')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'test://artifact.url')
        binding.setVariable('STAGE_NAME', 'test_stage')
        binding.setVariable('TEST_WORKLOAD', 'nyc-taxis')
        binding.setVariable('WEBHOOK_URL', 'test://artifact.url')
        binding.setVariable('TELEMETRY_PARAMS', '')

        super.setUp()
    }

    @Test
    public void testRunNonSecurityBenchmarkTestScript_verifyPipeline() {
        super.testPipeline("jenkins/opensearch/benchmark-test.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/opensearch/benchmark-test.jenkinsfile")
    }

    @Test
    void testRunNonSecurityBenchmarkTestScript_verifyArtifactDownloads() {
        runScript("jenkins/opensearch/benchmark-test.jenkinsfile")

        def curlCommands = getCommandExecutions('sh', 'curl').findAll {
            shCommand -> shCommand.contains('curl')
        }

        assertThat(curlCommands.size(), equalTo(3))
        assertThat(curlCommands, hasItem(
                "curl -sSL --retry 5 test://artifact.url --output tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml".toString()
        ))

        def s3DownloadCommands = getCommandExecutions('s3Download', 'bucket').findAll {
            shCommand -> shCommand.contains('bucket')
        }

        assertThat(s3DownloadCommands.size(), equalTo(2))
        assertThat(s3DownloadCommands, hasItems(
                "{file=config.yml, bucket=ARTIFACT_BUCKET_NAME, path=test_config/config.yml, force=true}".toString(),
                "{file=benchmark.ini, bucket=ARTIFACT_BUCKET_NAME, path=test_config/benchmark.ini, force=true}".toString()
        ))
    }

    @Test
    void testRunNonSecurityBenchmarkTestScript_verifyScriptExecutions() {
        runScript("jenkins/opensearch/benchmark-test.jenkinsfile")

        def testScriptCommands = getCommandExecutions('sh', './test.sh').findAll {
            shCommand -> shCommand.contains('./test.sh')
        }

        assertThat(testScriptCommands.size(), equalTo(1))
        assertThat(testScriptCommands, hasItem(
                "set +x && ./test.sh benchmark-test execute-test --bundle-manifest tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml    --config /tmp/workspace/config.yml --workload nyc-taxis --benchmark-config /tmp/workspace/benchmark.ini --user-tag distribution-build-id:1236,arch:x64,os-commit-id:22408088f002a4fc8cdd3b2ed7438866c14c5069,run-type:test,security-enabled:false,jenkins-build-id:307 --without-security     --use-50-percent-heap    --suffix 307 --manager-node-count 3 --data-node-count 3    --data-instance-type r5-4xlarge  --test-procedure append-no-conflicts --exclude-tasks type:search,scroll --include-tasks type:search,scroll  --data-node-storage 100".toString()
        ))
    }

    @Test
    void testRunSecurityBenchmarkTestScript_verifyJob_aborted() {
        binding.setVariable('BUNDLE_MANIFEST', 'tests/jenkins/data/opensearch-1.3.0-bundle.yml')
        binding.setVariable('HAS_SECURITY', true)
        helper.registerAllowedMethod("cfnDescribe", [Map.class]) { throw exception }
        helper.registerAllowedMethod('sh', [String.class], { String cmd ->
            updateBuildStatus('ABORTED')
        })
        runScript("jenkins/opensearch/benchmark-test.jenkinsfile")

        assertJobStatusAborted()
        assertCallStack()
        assertCallStack().contains("cfnDescribe({stack=opensearch-infra-stack-307-1234-x64})")
        assertCallStack().contains("Stack 'opensearch-infra-stack-307-1234-x64' does not exist, nothing to remove")
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
