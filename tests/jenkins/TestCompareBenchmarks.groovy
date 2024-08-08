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

class TestCompareBenchmarks extends BuildPipelineTest {
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
        helper.registerAllowedMethod("uploadTestResults", [Map])
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
        helper.registerAllowedMethod("throttleJobProperty", [Map])

        binding.setVariable('AGENT_LABEL', 'Jenkins-Agent-AL2-X64-M52xlarge-Docker-Host-Benchmark-Test')
        binding.setVariable('ARCHITECTURE', 'x64')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'test_bucket')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('env', ['BUILD_NUMBER': '307'])
        binding.setVariable('BUILD_URL', 'test://artifact.url')
        binding.setVariable('BUILD_NUMBER', '307')
        binding.setVariable('JOB_NAME', 'compare-benchmarks')
        binding.setVariable('BENCHMARK_TEST_CONFIG_LOCATION', 'test_config')
        binding.setVariable('PULL_REQUEST_NUMBER', '1234')
        binding.setVariable('pull_request', 1234)
        binding.setVariable('REPOSITORY','opensearch-project/OpenSearch')
        binding.setVariable('BASELINE_TEST_EXECUTION_ID', 'baseline-id')
        binding.setVariable('CONTENDER_TEST_EXECUTION_ID', 'contender-id')
    }

    @Test
    public void testCompareBenchmark_verifyPipeline() {

        super.testPipeline("jenkins/opensearch/benchmark-compare.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/opensearch/benchmark-compare.jenkinsfile")
    }

    @Test
    void testCompareBenchmark_verifyScriptExecutions() {
        runScript("jenkins/opensearch/benchmark-compare.jenkinsfile")

        def testScriptCommands = getCommandExecutions('sh', './test.sh').findAll {
            shCommand -> shCommand.contains('./test.sh')
        }
        assertThat(testScriptCommands.size(), equalTo(1))
        assertThat(testScriptCommands, hasItems("set +x && ./test.sh benchmark-test compare baseline-id contender-id --benchmark-config /tmp/workspace/benchmark.ini --suffix 307"))

        def testGhCliCommand = getCommandExecutions('sh', 'gh').findAll {
            shCommand -> shCommand.contains('gh')
        }
        assertThat(testGhCliCommand.size(), equalTo(1))
        assertThat(testGhCliCommand, hasItem('gh pr comment 1234 --repo opensearch-project/OpenSearch --body-file final_result_307.md'))
        assertCallStack().contains("benchmark-compare.runBenchmarkTestScript({command=compare, baseline=baseline-id, contender=contender-id, suffix=307})")
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
