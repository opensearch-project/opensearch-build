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
                .defaultVersion('7.2.0')
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
