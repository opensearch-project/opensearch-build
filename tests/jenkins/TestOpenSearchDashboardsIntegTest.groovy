/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.CoreMatchers.hasItems
import static org.hamcrest.MatcherAssert.assertThat
import static org.junit.jupiter.api.Assertions.assertThrows

class TestOpenSearchDashboardsIntegTest extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('5.11.1')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        super.setUp()

        def jobName = "dummy_job"
        def testManifest = "tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml"
        def buildId = 215
        def buildManifest = "tests/jenkins/data/opensearch-dashboards-3.0.0-build.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/3.0.0/${buildId}/linux/x64/tar/builds/opensearch-dashboards/opensearch-dashboards-3.0.0-linux-x64.tar.gz"
        def buildManifestOpenSearch = "tests/jenkins/data/opensearch-3.0.0-build.yml"
        def buildManifestUrlOpenSearch = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/3.0.0/${buildId}/linux/x64/tar/dist/opensearch/opensearch-3.0.0-linux-x64.tar.gz"
        def agentLabel = "Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host"
        def bucketName = 'job-s3-bucket-name'

        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'DUMMY_AWS_ACCOUNT_PUBLIC')
        binding.setVariable('env', ['BUILD_NUMBER': '215', 'PUBLIC_ARTIFACT_URL': 'DUMMY_PUBLIC_ARTIFACT_URL', 'JOB_NAME': 'dummy_job', 'DOCKER_AGENT':[image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11'] ])
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_BUCKET_NAME')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_ARTIFACT_BUCKET_NAME')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'DUMMY_PUBLIC_ARTIFACT_URL')
        binding.setVariable('STAGE_NAME', 'DUMMY_STAGE_NAME')
        binding.setVariable('JOB_NAME', 'dummy_job')
        binding.setVariable('distribution', 'tar')
        binding.setVariable('BUILD_URL', 'htth://BUILD_URL_dummy.com')
        binding.setVariable('WEBHOOK_URL', 'htth://WEBHOOK_URL_dummy.com')
        binding.setVariable('TEST_MANIFEST', testManifest)
        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('BUILD_MANIFEST_URL_OPENSEARCH', buildManifestUrlOpenSearch)
        binding.setVariable('BUILD_NUMBER', '215')
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)
        binding.setVariable('RUN_DISPLAY_URL', 'https://some/url/redirect')
        binding.setVariable('AGENT_LABEL', agentLabel)
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('BUILD_MANIFEST_OPENSEARCH', buildManifestOpenSearch)
        binding.setVariable('BUILD_ID', "${buildId}")
        binding.setVariable('distribution', 'tar' )
        binding.setVariable('COMPONENT_NAME', '' )
        binding.getVariable('currentBuild').upstreamBuilds = [[fullProjectName: jobName]]
        def env = binding.getVariable('env')
        env['DOCKER_AGENT'] = [image:'opensearchstaging/opensearchstaging/ci-runner:ci-runner-rockylinux8-opensearch-dashboards-integtest-v2', args:'-e JAVA_HOME=/opt/java/openjdk-11']
        env['PUBLIC_ARTIFACT_URL'] = 'DUMMY_PUBLIC_ARTIFACT_URL'
        env['JOB_NAME'] = 'dummy_job'

        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("withCredentials", [Map])

        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((this.testManifest ?: binding.getVariable('TEST_MANIFEST') as File).text)
        })

        helper.registerAllowedMethod('parameterizedCron', [String], null)
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((buildManifest as File).text)
        })
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.addFileExistsMock("manifests/${testManifest}", true)
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod('findFiles', [Map.class], null)
        helper.registerAllowedMethod('unstash', [String.class], null)
    }

    @Test
    void integTests_runs_for_all_components() {
        super.testPipeline('jenkins/opensearch-dashboards/integ-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch-dashboards/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('sh', 'test.sh'), hasItems(
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component ganttChartDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component anomalyDetectionDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component queryWorkbenchDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component reportsDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component observabilityDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString()
        ))
        assertThat(getCommandExecutions('sh', 'report.sh'), hasItems('./report.sh manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --artifact-paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/3.0.0/215/linux/x64/tar opensearch-dashboards=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/3.0.0/215/linux/x64/tar --test-run-id 215 --test-type integ-test --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '))
    }

    @Test
    void checkUploadResults() {
        runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('s3Upload', ''), hasItem('{file=test-results, bucket=ARTIFACT_BUCKET_NAME, path=dummy_job/3.0.0/215/linux/x64/tar/test-results}'))
    }

    @Test
    void checkIfRunningInParallel(){
        runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('parallel', ''), hasItem('{Run Integtest ganttChartDashboards=groovy.lang.Closure, Run Integtest indexManagementDashboards=groovy.lang.Closure, Run Integtest anomalyDetectionDashboards=groovy.lang.Closure, Run Integtest OpenSearch-Dashboards=groovy.lang.Closure, Run Integtest reportsDashboards=groovy.lang.Closure, Run Integtest queryWorkbenchDashboards=groovy.lang.Closure, Run Integtest observabilityDashboards=groovy.lang.Closure}'))
    }

    @Test
    void checkError() {
        helper.addFileExistsMock('manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml', false)
        runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('error', ''), hasItem('Integration Tests failed to start. Test manifest was not provided or not found in manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml.'))
        assertJobStatusFailure()
    }

    @Test
    void checkGHissueCreation() {
        helper.addShMock("date -d \"3 days ago\" +'%Y-%m-%d'") { script ->
            return [stdout: "2023-10-24", exitValue: 0]
        }
        helper.addShMock("""gh issue list --repo https://github.com/opensearch-project/dashboards-visualizations.git -S "[AUTOCUT] Integration Test failed for ganttChartDashboards: 3.0.0 tar distribution in:title" --label autocut,v3.0.0,integ-test-failure --json number --jq '.[0].number'""") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("""gh issue list --repo https://github.com/opensearch-project/dashboards-visualizations.git -S "[AUTOCUT] Integration Test failed for ganttChartDashboards: 3.0.0 tar distribution in:title is:closed closed:>=2023-10-24" --label autocut,v3.0.0,integ-test-failure --json number --jq '.[0].number'""") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock('env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component ganttChartDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar ', '', 1)
        assertThrows(Exception) {
            runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        }
        assertJobStatusFailure()
        assertThat(getCommandExecutions('sh', 'script'), hasItem("{script=gh issue list --repo https://github.com/opensearch-project/dashboards-observability.git -S \"[AUTOCUT] Integration Test failed for observabilityDashboards: 3.0.0 tar distribution in:title\" --label autocut,v3.0.0,integ-test-failure --json number --jq '.[0].number', returnStdout=true}"))
    }

    @Test
    void CheckCloseGHissue() {
        helper.addShMock("date -d \"3 days ago\" +'%Y-%m-%d'") { script ->
            return [stdout: "2023-10-24", exitValue: 0]
        }
        helper.addShMock('env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component observabilityDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar ', '', 1)
        helper.addShMock('gh issue list --repo https://github.com/opensearch-project/dashboards-visualization.git -S "[AUTOCUT] Integration Test failed for ganttChartDashboards: 3.0.0 tar distribution in:title" --label autocut,v3.0.0,integ-test-failure', '', 0)
        assertThrows(Exception) {
            runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        }
        assertJobStatusFailure()
        runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('sh', 'script'), hasItem("{script=gh issue list --repo https://github.com/opensearch-project/dashboards-visualizations.git -S \"[AUTOCUT] Integration Test failed for ganttChartDashboards: 3.0.0 tar distribution in:title\" --label autocut,v3.0.0,integ-test-failure --json number --jq '.[0].number', returnStdout=true}"))
        assertThat(getCommandExecutions('sh', 'script'), hasItem("{script=gh issue close bbb\nccc -R opensearch-project/dashboards-visualizations --comment \"Closing the issue as the Integration Test passed for ganttChartDashboards<br>Version: 3.0.0<br>Distribution: tar<br>Architecture: x64<br>Platform: linux<br><br>Please check the logs: https://some/url/redirect<br><br> *\", returnStdout=true}"))
    }

    @Test
    void checkGHexistingIssue() {
        helper.addShMock("date -d \"3 days ago\" +'%Y-%m-%d'") { script ->
            return [stdout: "2023-10-24", exitValue: 0]
        }
        helper.addShMock("""gh issue list --repo https://github.com/opensearch-project/dashboards-observability.git -S "[AUTOCUT] Integration Test failed for observabilityDashboards: 3.0.0 tar distribution in:title is:closed closed:>=2023-10-24" --label autocut,v3.0.0,integ-test-failure --json number --jq '.[0].number'""") { script ->
            return [stdout: "", exitValue: 0]
        }
        helper.addShMock("""gh issue list --repo https://github.com/opensearch-project/sql.git -S "[AUTOCUT] Integration Test failed for observabilityDashboards: 3.0.0 tar distribution in:title" --label autocut,v3.0.0,integ-test-failure --json number --jq '.[0].number'""") { script ->
            return [stdout: "22", exitValue: 0]
        }
        helper.addShMock('env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component observabilityDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar ', '', 1)
        assertThrows(Exception) {
            runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        }
        assertJobStatusFailure()
        assertThat(getCommandExecutions('println', 'Issue'), hasItem('Issue already exists, adding a comment'))
        assertThat(getCommandExecutions('sh', 'script'), hasItem("{script=gh issue comment bbb\nccc --repo https://github.com/opensearch-project/dashboards-observability.git --body \"The integration test failed at distribution level for component observabilityDashboards<br>Version: 3.0.0<br>Distribution: tar<br>Architecture: x64<br>Platform: linux<br><br>Please check the logs: https://some/url/redirect<br><br> * Test-report manifest:*<br> - https://ci.opensearch.org/ci/dbc/dummy_job/3.0.0/215/linux/x64/tar/test-results/215/integ-test/test-report.yml <br><br> _Note: Steps to reproduce, additional logs and other files can be found within the above test-report manifest. <br>Instructions of this test-report manifest can be found [here](https://github.com/opensearch-project/opensearch-build/tree/main/src/report_workflow#guide-on-test-report-manifest-from-ci)._\", returnStdout=true}"))
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
