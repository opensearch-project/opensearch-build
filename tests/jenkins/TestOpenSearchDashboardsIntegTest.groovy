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
                .defaultVersion('4.1.1')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        super.setUp()

        def jobName = "dummy_job"
        def testManifest = "tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml"
        def buildId = 215
        def buildManifest = "tests/jenkins/data/opensearch-dashboards-1.2.0-build.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/1.2.0/${buildId}/linux/x64/tar/builds/opensearch-dashboards/opensearch-dashboards-1.2.0-linux-x64.tar.gz"
        def agentLabel = "Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host"
        def bucketName = 'job-s3-bucket-name'

        binding.setVariable('env', ['BUILD_NUMBER': '215'])
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_BUCKET_NAME')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'DUMMY_AWS_ACCOUNT_PUBLIC')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_ARTIFACT_BUCKET_NAME')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'DUMMY_PUBLIC_ARTIFACT_URL')
        binding.setVariable('env', ['BUILD_NUMBER': '215'])
        binding.setVariable('STAGE_NAME', 'DUMMY_STAGE_NAME')
        binding.setVariable('JOB_NAME', 'dummy_job')
        binding.setVariable('distribution', 'tar')
        binding.setVariable('BUILD_NUMBER', '215')
        binding.setVariable('BUILD_URL', 'htth://BUILD_URL_dummy.com')
        binding.setVariable('WEBHOOK_URL', 'htth://WEBHOOK_URL_dummy.com')
        binding.setVariable('TEST_MANIFEST', testManifest)
        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('AGENT_LABEL', agentLabel)
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('BUILD_ID', "${buildId}")
        def env = binding.getVariable('env')
        env['DOCKER_AGENT'] = [image:'opensearchstaging/opensearchstaging/ci-runner:ci-runner-rockylinux8-opensearch-dashboards-integtest-v2', args:'-e JAVA_HOME=/opt/java/openjdk-11']
        binding.getVariable('currentBuild').upstreamBuilds = [[fullProjectName: jobName]]

        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("withCredentials", [Map])

        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((this.testManifest ?: binding.getVariable('TEST_MANIFEST') as File).text)
        })
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
        helper.registerAllowedMethod('fileExists', [String.class], { args ->
            return true;
        })

        helper.registerAllowedMethod('findFiles', [Map.class], null)
        helper.registerAllowedMethod('unstash', [String.class], null)
    }

    @Test
    void integTests_runs_for_all_components() {
        super.testPipeline('jenkins/opensearch-dashboards/integ-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch-dashboards/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('sh', 'test.sh'), hasItems(
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component ganttChartDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component indexManagementDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component anomalyDetectionDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component securityDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component functionalTestDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component OpenSearch-Dashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component alertingDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component queryWorkbenchDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component reportsDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString(),
                'env PATH=$PATH  ./test.sh integ-test manifests/tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml --component observabilityDashboards --test-run-id 215 --paths opensearch=/tmp/workspace/tar opensearch-dashboards=/tmp/workspace/tar '.toString()
        ))
    }

    @Test
    void checkUploadResults() {
        runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('s3Upload', ''), hasItem('{file=test-results, bucket=ARTIFACT_BUCKET_NAME, path=dummy_job/1.2.0/215/linux/x64/tar/test-results}'))
    }

    @Test
    void checkIfRunningInParallel(){
        runScript('jenkins/opensearch-dashboards/integ-test.jenkinsfile')
        assertThat(getCommandExecutions('parallel', ''), hasItem('{Run Integtest ganttChartDashboards=groovy.lang.Closure, Run Integtest indexManagementDashboards=groovy.lang.Closure, Run Integtest anomalyDetectionDashboards=groovy.lang.Closure, Run Integtest OpenSearch-Dashboards=groovy.lang.Closure, Run Integtest securityDashboards=groovy.lang.Closure, Run Integtest functionalTestDashboards=groovy.lang.Closure, Run Integtest alertingDashboards=groovy.lang.Closure, Run Integtest queryWorkbenchDashboards=groovy.lang.Closure, Run Integtest reportsDashboards=groovy.lang.Closure, Run Integtest observabilityDashboards=groovy.lang.Closure}'))
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
