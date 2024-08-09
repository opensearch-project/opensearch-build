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

class TestBenchmarkPullRequest extends BuildPipelineTest {
    @Override
    @Before
    void setUp() {
        super.setUp()

        helper.registerSharedLibrary(
                library().name('jenkins')
                        .defaultVersion('6.8.2')
                        .allowOverride(true)
                        .implicit(true)
                        .targetPath('vars')
                        .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                        .build()
        )

        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod('unstash', [String.class], null)
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
        helper.registerAllowedMethod("throttleJobProperty", [Map])

        binding.setVariable('AGENT_LABEL', 'Jenkins-Agent-AL2-X64-M52xlarge-Docker-Host-Benchmark-Test')
        binding.setVariable('ARCHITECTURE', 'x64')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'test_bucket')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('env', ['BUILD_NUMBER': '307'])
        binding.setVariable('BUILD_NUMBER', '307')
        binding.setVariable('BUILD_URL', 'test://artifact.url')
        binding.setVariable('BUILD_ID', '1234')
        binding.setVariable('BUNDLE_MANIFEST', '')
        binding.setVariable('BUNDLE_MANIFEST_URL', '')
        binding.setVariable('DISTRIBUTION_URL', 'https://artifacts.com/artifact.tar.gz')
        binding.setVariable('DISTRIBUTION_VERSION', '3.0.0')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'bot_token_name')
        binding.setVariable('GITHUB_USER', 'test_user')
        binding.setVariable('GITHUB_TOKEN', 'test_token')
        binding.setVariable('HAS_SECURITY', 'false')
        binding.setVariable('SINGLE_NODE_CLUSTER', 'true')
        binding.setVariable('MIN_DISTRIBUTION', 'true')
        binding.setVariable('USE_50_PERCENT_HEAP', 'true')
        binding.setVariable('SUFFIX', '1234')
        binding.setVariable('MANAGER_NODE_COUNT', '')
        binding.setVariable('DATA_NODE_COUNT', '')
        binding.setVariable('ENABLE_REMOTE_STORE', 'false')
        binding.setVariable('USER_TAGS', 'run-type:test')
        binding.setVariable('WORKLOAD_PARAMS', '')
        binding.setVariable('TEST_PROCEDURE', 'append-no-conflicts')
        binding.setVariable('EXCLUDE_TASKS', '')
        binding.setVariable('INCLUDE_TASKS', '')
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
        binding.setVariable('pull_request_number', '1234')
        binding.setVariable('pull_request', 1234)
        binding.setVariable('baseline_cluster_config', 'test-cluster-config')
        binding.setVariable('repository','opensearch-project/OpenSearch')

        helper.registerAllowedMethod("GenericTrigger", [Map], { println 'GenericTrigger called with params: ' + it })
        helper.registerAllowedMethod("sh", [Map.class], { map ->
            return '{"hits":{"total":{"value":1},"hits":[{"_source":{"test-execution-id":"test-id"}}]}}'
        })
    }

    @Test
    public void testBenchmarkPullRequestGenericCause_verifyPipeline() {
        binding.getVariable('currentBuild').rawBuild = [:]
        binding.getVariable('currentBuild').rawBuild.getCauses = { return "jenkins.branch.GenericCause@123abc" }
        helper.registerAllowedMethod('getCompareBenchmarkIds', [Map.class], { params ->
            return [baseline: "mockBaseline", contender: "mockContender"]
        })

        super.testPipeline("jenkins/opensearch/benchmark-pull-request.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/opensearch/benchmark-pull-request-generic.jenkinsfile")
    }

    @Test
    public void testBenchmarkPullRequestUserIdCause_verifyPipeline() {
        binding.getVariable('currentBuild').rawBuild = [:]
        binding.getVariable('currentBuild').rawBuild.getCauses = { return "jenkins.branch.UserIdCause@123abc" }

        super.testPipeline("jenkins/opensearch/benchmark-pull-request.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/opensearch/benchmark-pull-request-user.jenkinsfile")
    }

    @Test
    void testBenchmarkPullRequest_verifyScriptExecutions() {
        binding.getVariable('currentBuild').rawBuild = [:]
        binding.getVariable('currentBuild').rawBuild.getCauses = { return "jenkins.branch.GenericCause@123abc" }

        runScript("jenkins/opensearch/benchmark-pull-request.jenkinsfile")

        def testScriptCommands = getCommandExecutions('sh', './test.sh').findAll {
            shCommand -> shCommand.contains('./test.sh')
        }
        assertThat(testScriptCommands.size(), equalTo(1))
        assertThat(testScriptCommands, hasItems(
                "set +x && ./test.sh benchmark-test execute-test  --distribution-url https://artifacts.com/artifact.tar.gz --distribution-version 3.0.0  --config /tmp/workspace/config.yml --workload nyc-taxis --benchmark-config /tmp/workspace/benchmark.ini --user-tag run-type:test,security-enabled:false --without-security   --single-node --min-distribution --use-50-percent-heap    --suffix 307      --data-instance-type r5-4xlarge  --test-procedure append-no-conflicts    --data-node-storage 100".toString()
        ))

        def testGhCliCommand = getCommandExecutions('sh', 'gh').findAll {
            shCommand -> shCommand.contains('gh')
        }
        assertThat(testGhCliCommand.size(), equalTo(1))
        assertThat(testGhCliCommand, hasItem('gh pr comment 1234 --repo opensearch-project/OpenSearch --body-file final_result_307.md'))
        assertCallStack().contains(" benchmark-pull-request.getCompareBenchmarkIds({baselineClusterConfig=test-cluster-config, distributionVersion=3.0.0-SNAPSHOT, workload=nyc-taxis, pullRequestNumber=1234})")
    }

    @Test
    void testBenchmarkPullRequest_verifyJob_failure(){

        binding.getVariable('currentBuild').rawBuild = [:]
        binding.getVariable('currentBuild').rawBuild.getCauses = { return "jenkins.branch.GenericCause@123abc" }
        helper.registerAllowedMethod('sh', [String.class], { String cmd ->
            updateBuildStatus('FAILURE')
        })
        def result = runScript("jenkins/opensearch/benchmark-pull-request.jenkinsfile")

        assertJobStatusFailure()
        assertCallStack()
        assertCallStack().contains("gh pr comment 1234 --repo opensearch-project/OpenSearch --body \"The benchmark job test://artifact.url failed.\n Please see logs to debug.\"")
    }

    @Test
    void testBenchmarkPullRequest_verifyJob_aborted() throws Exception {

        binding.getVariable('currentBuild').rawBuild = [:]
        binding.getVariable('currentBuild').rawBuild.getCauses = { return "jenkins.branch.GenericCause@123abc" }
        helper.registerAllowedMethod("cfnDescribe", [Map.class]) { args -> return true}
        helper.registerAllowedMethod('sh', [String.class], { String cmd ->
            updateBuildStatus('ABORTED')
        })
        runScript("jenkins/opensearch/benchmark-pull-request.jenkinsfile")

        assertJobStatusAborted()
        assertCallStack()
        assertCallStack().contains("cfnDescribe({stack=opensearch-infra-stack-307})")
        assertCallStack().contains("cfnDelete({stack=opensearch-infra-stack-307, pollInterval=1000})")
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
