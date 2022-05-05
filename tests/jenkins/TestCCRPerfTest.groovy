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

class TestCCRPerfTest extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new RunPerfTestScriptLibTester(
            'tests/jenkins/data/opensearch-1.3.0-bundle.yml',
            '1236',
            '',
            '',
            '',
            '',
            true
        ))
        super.setUp()
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
            "{file=config.yml, bucket=test_bucket, path=test_config/config-ccr.yml, force=true}".toString()
        ))
    }

    @Test
    void testCCRPerfTestScript_verifyPackageInstallation() {
        runScript("jenkins/cross-cluster-replication/perf-test.jenkinsfile")

        def npmCommands = getCommandExecutions('sh', 'npm').findAll {
            shCommand -> shCommand.contains('npm')
        }

        assertThat(npmCommands.size(), equalTo(1))

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
            "{file=test-results, bucket=test_bucket, path=perf-test/1.3.0/1236/linux/x64/tar/test-results}".toString()
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