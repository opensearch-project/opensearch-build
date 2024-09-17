/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.CoreMatchers.not
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.MatcherAssert.assertThat
import static org.junit.jupiter.api.Assertions.assertThrows

class TestOpenSearchIntegTest extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('6.9.1')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()

        def jobName = "dummy_job"
        def testManifest = "tests/jenkins/data/opensearch-3.0.0-test.yml"
        def buildManifest = "tests/jenkins/data/opensearch-3.0.0-build.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/3.0.0/9010/linux/x64/tar/dist/opensearch/opensearch-3.0.0-linux-x64.tar.gz"
        def agentLabel = "Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host"
        def bucketName = 'job-s3-bucket-name'

        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('env', ['BUILD_NUMBER': '234', 'PUBLIC_ARTIFACT_URL': 'DUMMY_PUBLIC_ARTIFACT_URL', 'JOB_NAME': 'dummy_job', 'DOCKER_AGENT':[image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11']])
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_BUCKET_NAME')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'DUMMY_AWS_ACCOUNT_PUBLIC')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_ARTIFACT_BUCKET_NAME')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'DUMMY_PUBLIC_ARTIFACT_URL')
        binding.setVariable('STAGE_NAME', 'DUMMY_STAGE_NAME')
        binding.setVariable('JOB_NAME', 'dummy_job')
        binding.setVariable('BUILD_URL', 'htth://BUILD_URL_dummy.com')
        binding.setVariable('WEBHOOK_URL', 'htth://WEBHOOK_URL_dummy.com')
        binding.setVariable('TEST_MANIFEST', testManifest)
        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('AGENT_LABEL', agentLabel)
        binding.setVariable('BUILD_NUMBER', '234')
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)
        binding.setVariable('RUN_DISPLAY_URL', 'https://some/url/redirect')
        binding.setVariable('distribution', 'tar' )
        binding.setVariable('COMPONENT_NAME', '' )
        binding.setVariable('RC_NUMBER', '0')
        binding.getVariable('currentBuild').upstreamBuilds = [[fullProjectName: jobName]]
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withCredentials", [Map])
        helper.registerAllowedMethod('parameterizedCron', [String], null)
        helper.registerAllowedMethod("readYaml", [Map.class], { args ->
            if (args.file == 'manifests/tests/jenkins/data/opensearch-3.0.0-test.yml') {
                return new Yaml().load((testManifest as File).text)
            } else if (args.file == 'tests/jenkins/data/opensearch-3.0.0-build.yml') {
                return new Yaml().load((buildManifest as File).text)
            } else {
                println("Manifest not found ${args.file}")
            }
        })
        helper.addFileExistsMock("manifests/${testManifest}", true)
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod('findFiles', [Map.class], null)
        helper.registerAllowedMethod('unstash', [String.class], null)
    }

    @Test
    void integTests_runs_consistently() {
        addParam('UPDATE_GITHUB_ISSUES', true)
        super.testPipeline('jenkins/opensearch/integ-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch/integ-test.jenkinsfile')
        assert getCommandExecutions('stage', 'validate-artifacts').size() == 1
        assertThat(getCommandExecutions('sh', 'test.sh'), hasItem('env PATH=$PATH JAVA_HOME=/opt/java/openjdk-17 ./test.sh integ-test manifests/tests/jenkins/data/opensearch-3.0.0-test.yml --component k-NN --test-run-id 234 --paths opensearch=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/9010/linux/x64/tar '))
        assertThat(getCommandExecutions('sh', 'report.sh'), hasItem('./report.sh manifests/tests/jenkins/data/opensearch-3.0.0-test.yml --artifact-paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/3.0.0/9010/linux/x64/tar --test-run-id 234 --test-type integ-test --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/9010/linux/x64/tar --release-candidate 0 '))
        assertThat(getCommandExecutions('echo', 'Testing'), hasItem('Testing components: [ml-commons, anomaly-detection, neural-search, security-analytics, security, k-NN, notifications]'))
        assertCallStack().contains('curl -sSL https://ci.opensearch.org/ci/dbc/integ-test/3.0.0/9010/linux/x64/tar/test-results/234/integ-test/test-report.yml --output test-results-os-234/test-report.yml')
        assertCallStack().contains('{distributionBuildUrl=https://build.ci.opensearch.org/blue/organizations/jenkins/distribution-build-opensearch/detail/distribution-build-opensearch/9010/pipeline, jobName=dummy_job, testReportManifestYml=test-results-os-234/test-report.yml}')
    }

    @Test
    void checkUploadResults() {
        runScript('jenkins/opensearch/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('s3Upload', ''), hasItem('{file=test-results, bucket=ARTIFACT_BUCKET_NAME, path=dummy_job/3.0.0/9010/linux/x64/tar/test-results}'))
    }

    @Test
    void checkError() {
        helper.addFileExistsMock('manifests/tests/jenkins/data/opensearch-3.0.0-test.yml', false)
        runScript('jenkins/opensearch/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('error', ''), hasItem('Integration Tests failed to start. Test manifest was not provided or not found in manifests/tests/jenkins/data/opensearch-3.0.0-test.yml.'))
        assertJobStatusFailure()
    }

    @Test
    void checkErrorForMissingComponentFromTestManifest() {
        addParam('COMPONENT_NAME', 'sql')
        runScript('jenkins/opensearch/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('echo', 'sql'), hasItem('Skipping tests for sql as is not present in the provided build manifest.'))
    }

    @Test
    void checkGHissueCreation() {
        addParam('UPDATE_GITHUB_ISSUES', true)
        helper.addShMock("date -d \"3 days ago\" +'%Y-%m-%d'") { script ->
            return [stdout: "2023-10-24", exitValue: 0]
        }
        helper.addShMock("""env PATH=\$PATH JAVA_HOME=/opt/java/openjdk-17 ./test.sh integ-test manifests/tests/jenkins/data/opensearch-3.0.0-test.yml --component k-NN --test-run-id 234 --paths opensearch=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/9010/linux/x64/tar """) { script ->
            return [stdout: "Error running integtest for component k-NN, creating Github issue", exitValue: 1]}
        helper.addShMock("""gh issue list --repo https://github.com/opensearch-project/k-NN.git -S "[AUTOCUT] Integration Test failed for k-NN: 3.0.0 in:title" --json number --jq '.[0].number'""") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("""gh issue list --repo https://github.com/opensearch-project/k-NN.git -S "[AUTOCUT] Integration Test failed for k-NN: 3.0.0 in:title is:closed closed:>=2023-10-24" --json number --jq '.[0].number'""") { script ->
            return [stdout: "", exitValue: 0]
        }
        assertThrows(Exception) {
            runScript('jenkins/opensearch/integ-test.jenkinsfile')
        }
        assertJobStatusFailure()
        assertThat(getCommandExecutions('sh', 'script'), hasItem("""{script=gh issue create --title \"[AUTOCUT] Integration Test failed for k-NN: 3.0.0\" --body \"The integration test failed at distribution level for component k-NN<br>Version: 3.0.0<br>Distribution: tar<br>Architecture: x64<br>Platform: linux<br><br>Please check the logs: https://some/url/redirect<br><br> * Test-report manifest:*<br> - https://ci.opensearch.org/ci/dbc/dummy_job/3.0.0/9010/linux/x64/tar/test-results/234/integ-test/test-report.yml <br><br> _Note: Steps to reproduce, additional logs and other files can be found within the above test-report manifest. <br>Instructions of this test-report manifest can be found [here](https://github.com/opensearch-project/opensearch-build/tree/main/src/report_workflow#guide-on-test-report-manifest-from-ci)._\" --label \"autocut,v3.0.0\" --label \"untriaged\" --repo https://github.com/opensearch-project/k-NN.git, returnStdout=true}"""))
    }

    @Test
    void CheckNotClosingGHissue() {
        addParam('UPDATE_GITHUB_ISSUES', true)
        helper.addShMock("date -d \"5 days ago\" +'%Y-%m-%d'") { script ->
            return [stdout: "2023-10-24", exitValue: 0]
        }
        helper.addShMock("""env PATH=\$PATH JAVA_HOME=/opt/java/openjdk-17 ./test.sh integ-test manifests/tests/jenkins/data/opensearch-3.0.0-test.yml --component k-NN --test-run-id 234 --paths opensearch=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/8184/linux/x64/tar""") { script -> 
        return [stdout: "Completed running integtest for component k-NN", exitValue: 0]
        }
        runScript('jenkins/opensearch/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('sh', 'script'), not(hasItem("{script=gh issue close bbb\nccc -R opensearch-project/k-NN --comment \"Closing the issue as the Integration Test passed for k-NN<br>Version: 3.0.0<br>Distribution: tar<br>Architecture: x64<br>Platform: linux<br><br>Please check the logs: https://some/url/redirect<br><br> *\", returnStdout=true}")))
    }

    @Test
    void checkGHexistingIssue() {
        addParam('UPDATE_GITHUB_ISSUES', true)
        helper.addShMock("date -d \"3 days ago\" +'%Y-%m-%d'") { script ->
            return [stdout: "2023-10-24", exitValue: 0]
        }
        helper.addShMock('env PATH=$PATH JAVA_HOME=/opt/java/openjdk-17 ./test.sh integ-test manifests/tests/jenkins/data/opensearch-3.0.0-test.yml --component k-NN --test-run-id 234 --paths opensearch=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/9010/linux/x64/tar ', '', 1)
        assertThrows(Exception) {
            runScript('jenkins/opensearch/integ-test.jenkinsfile')
        }
        assertJobStatusFailure()
        assertThat(getCommandExecutions('println', 'Issue'), hasItem('Issue already exists, adding a comment'))
        assertThat(getCommandExecutions('sh', 'script'), hasItem("{script=gh issue list --repo https://github.com/opensearch-project/k-NN.git -S \"[AUTOCUT] Integration Test failed for k-NN: 3.0.0 in:title\" --json number --jq '.[0].number', returnStdout=true}"))
        assertThat(getCommandExecutions('sh', 'script'), hasItem("{script=gh issue comment bbb\nccc --repo https://github.com/opensearch-project/k-NN.git --body \"The integration test failed at distribution level for component k-NN<br>Version: 3.0.0<br>Distribution: tar<br>Architecture: x64<br>Platform: linux<br><br>Please check the logs: https://some/url/redirect<br><br> * Test-report manifest:*<br> - https://ci.opensearch.org/ci/dbc/dummy_job/3.0.0/9010/linux/x64/tar/test-results/234/integ-test/test-report.yml <br><br> _Note: Steps to reproduce, additional logs and other files can be found within the above test-report manifest. <br>Instructions of this test-report manifest can be found [here](https://github.com/opensearch-project/opensearch-build/tree/main/src/report_workflow#guide-on-test-report-manifest-from-ci)._\", returnStdout=true}"))
    }

    @Test
    void checkGHIssueDisable() {
        addParam('COMPONENT_NAME', 'k-NN')
        helper.addShMock("""env PATH=\$PATH JAVA_HOME=/opt/java/openjdk-17 ./test.sh integ-test manifests/tests/jenkins/data/opensearch-3.0.0-test.yml --component k-NN --test-run-id 234 --paths opensearch=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/9010/linux/x64/tar """) { script ->
            return [stdout: "Error running integtest for component k-NN, creating Github issue", exitValue: 1]}
        assertThrows(Exception) {
            runScript('jenkins/opensearch/integ-test.jenkinsfile')
        }
        assertJobStatusFailure()
        assertThat(getCommandExecutions('sh', 'gh issue').size(), equalTo(0))
    }

    @Test
    void verifyLabelRemoval() {
        addParam('UPDATE_GITHUB_ISSUES', true)
        helper.addShMock("""gh issue list --repo https://github.com/opensearch-project/k-NN.git -S "[AUTOCUT] Integration Test failed for k-NN: 3.0.0 in:title" --json number --jq '.[0].number'""") { script ->
            return [stdout: "67", exitValue: 0]
        }
        helper.addShMock("""gh label list --repo https://github.com/opensearch-project/k-NN.git -S linux:tar:x64 --json name --jq '.[0].name'""") { script ->
            return [stdout: "linux:tar:x64", exitValue: 0]
        }
        helper.addShMock("""env PATH=\$PATH JAVA_HOME=/opt/java/openjdk-17 ./test.sh integ-test manifests/tests/jenkins/data/opensearch-3.0.0-test.yml --component k-NN --test-run-id 234 --paths opensearch=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/8184/linux/x64/tar""") { script -> 
        return [stdout: "Completed running integtest for component k-NN", exitValue: 0]
        }
        runScript('jenkins/opensearch/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('sh', 'gh issue'), hasItem('{script=gh issue edit 67 -R https://github.com/opensearch-project/k-NN.git --remove-label \"linux:tar:x64\", returnStdout=true}'))
    }

    @Test
    void verifyLabelAddition() {
        addParam('UPDATE_GITHUB_ISSUES', true)
        helper.addShMock("""env PATH=\$PATH JAVA_HOME=/opt/java/openjdk-17 ./test.sh integ-test manifests/tests/jenkins/data/opensearch-3.0.0-test.yml --component k-NN --test-run-id 234 --paths opensearch=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/9010/linux/x64/tar """) { script ->
            return [stdout: "Error running integtest for component k-NN, creating Github issue", exitValue: 1]}
        helper.addShMock("""gh issue list --repo https://github.com/opensearch-project/k-NN.git -S "[AUTOCUT] Integration Test failed for k-NN: 3.0.0 in:title" --json number --jq '.[0].number'""") { script ->
            return [stdout: "99", exitValue: 0]
        }
        helper.addShMock("""gh label list --repo https://github.com/opensearch-project/k-NN.git -S linux:tar:x64 --json name --jq '.[0].name'""") { script ->
            return [stdout: "no labels in opensearch-project/k-NN matched your search", exitValue: 0]
        }
        assertThrows(Exception) {
            runScript('jenkins/opensearch/integ-test.jenkinsfile')
        }
        assertJobStatusFailure()
        assertThat(getCommandExecutions('sh', 'label'), hasItem("{script=gh label create linux:tar:x64 --repo https://github.com/opensearch-project/k-NN.git, returnStdout=true}"))
        assertThat(getCommandExecutions('sh', 'gh issue'), hasItem('{script=gh issue edit 99 -R https://github.com/opensearch-project/k-NN.git --add-label \"linux:tar:x64\", returnStdout=true}'))
    }

    @Test
    void whenValidationIsNotChecked() {
        addParam('VALIDATE_ARTIFACTS', false)
        super.testPipeline('jenkins/opensearch/integ-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch/integ-test-without-validation.jenkinsfile')
        assert getCommandExecutions('stage', 'validate-artifacts').size() == 0
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
