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
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.not
import static org.hamcrest.CoreMatchers.hasItems
import static org.hamcrest.MatcherAssert.assertThat
import static org.junit.jupiter.api.Assertions.assertThrows

class TestOpenSearchDashboardsIntegTest extends BuildPipelineTest {

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
        binding.setVariable('RC_NUMBER', '0')
        def env = binding.getVariable('env')
        env['DOCKER_AGENT'] = [image:'opensearchstaging/opensearchstaging/ci-runner:ci-runner-almallinux8-opensearch-dashboards-integtest-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11']
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

///
    @Test
    void integTests_runs_for_all_components() {
        super.testPipeline('jenkins/opensearch-dashboards/integ-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch-dashboards/integ-test.jenkinsfile')
        assert getCommandExecutions('stage', 'validate-artifacts').size() == 1
        assertThat(getCommandExecutions('sh', 'test.sh'), hasItems(
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component ganttChartDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component anomalyDetectionDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component queryWorkbenchDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component reportsDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --component observabilityDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar '.toString()
        ))
        assertThat(getCommandExecutions('sh', 'report.sh'), hasItems('./report.sh manifests/tests/jenkins/data/opensearch-dashboards-3.0.0-test.yml --artifact-paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/3.0.0/215/linux/x64/tar opensearch-dashboards=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/3.0.0/215/linux/x64/tar --test-run-id 215 --test-type integ-test --base-path DUMMY_PUBLIC_ARTIFACT_URL/dummy_job/3.0.0/215/linux/x64/tar --release-candidate 0 '))
        assertCallStack().contains('curl -sSL https://ci.opensearch.org/ci/dbc/integ-test-opensearch-dashboards/3.0.0/215/linux/x64/tar/test-results/215/integ-test/test-report.yml --output test-results-osd-215/test-report.yml')
        assertCallStack().contains('{distributionBuildUrl=https://build.ci.opensearch.org/blue/organizations/jenkins/distribution-build-opensearch-dashboards/detail/distribution-build-opensearch-dashboards/215/pipeline, jobName=dummy_job, testReportManifestYml=test-results-osd-215/test-report.yml}')
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
    void whenValidationIsNotChecked() {
        addParam('VALIDATE_ARTIFACTS', false)
        super.testPipeline('jenkins/opensearch-dashboards/integ-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch-dashboards/integ-test-without-validation.jenkinsfile')
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
