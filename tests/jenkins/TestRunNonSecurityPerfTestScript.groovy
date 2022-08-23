/*
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

class TestRunNonSecurityPerfTestScript extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new RunPerfTestScriptLibTester(
            'tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml',
            '1236',
            'true',
            'nyc_taxis',
            '1',
            '1',
            false
        ))
        super.setUp()
    }

    @Test
    public void testRunNonSecurityPerfTestScript_verifyPipeline() {
        super.testPipeline("jenkins/opensearch/perf-test.jenkinsfile",
        "tests/jenkins/jenkinsjob-regression-files/opensearch/perf-test.jenkinsfile")
    }

    @Test
    void testRunNonSecurityPerfTestScript_verifyArtifactDownloads() {
        runScript("jenkins/opensearch/perf-test.jenkinsfile")

        def curlCommands = getCommandExecutions('sh', 'curl').findAll {
            shCommand -> shCommand.contains('curl')
        }

        assertThat(curlCommands.size(), equalTo(3))
        assertThat(curlCommands, hasItem(
            "curl -sSL test://artifact.url --output tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml".toString()
        ))

        def s3DownloadCommands = getCommandExecutions('s3Download', 'bucket').findAll {
            shCommand -> shCommand.contains('bucket')
        }

        assertThat(s3DownloadCommands.size(), equalTo(1))
        assertThat(s3DownloadCommands, hasItem(
            "{file=config.yml, bucket=ARTIFACT_BUCKET_NAME, path=test_config/config.yml, force=true}".toString()
        ))
    }

    @Test
    void testRunNonSecurityPerfTestScript_verifyPackageInstallation() {
        runScript("jenkins/opensearch/perf-test.jenkinsfile")

        def pipenvCommands = getCommandExecutions('sh', 'pipenv').findAll {
            shCommand -> shCommand.contains('pipenv')
        }

        assertThat(pipenvCommands.size(), equalTo(1))

    }

    @Test
    void testRunNonSecurityPerfTestScript_verifyScriptExecutions() {
        runScript("jenkins/opensearch/perf-test.jenkinsfile")

        def testScriptCommands = getCommandExecutions('sh', './test.sh').findAll {
            shCommand -> shCommand.contains('./test.sh')
        }

        assertThat(testScriptCommands.size(), equalTo(1))
        assertThat(testScriptCommands, hasItem(
            "./test.sh perf-test --stack test-single-1236-x64-307 --bundle-manifest tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml --config config.yml --without-security --workload nyc_taxis --test-iters 1 --warmup-iters 1 ".toString()
        ))

        def resultUploadScriptCommands = getCommandExecutions('s3Upload', 'test-results').findAll {
            shCommand -> shCommand.contains('test-results')
        }
        assertThat(resultUploadScriptCommands.size(), equalTo(1))
        assertThat(resultUploadScriptCommands, hasItem(
            "{file=test-results, bucket=ARTIFACT_BUCKET_NAME, path=perf-test/1.3.0/1236/linux/x64/tar/307/test-results}".toString()
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