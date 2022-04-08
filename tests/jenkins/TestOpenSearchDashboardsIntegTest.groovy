/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml

class TestOpenSearchDashboardsIntegTest extends BuildPipelineTest {

    @Before
    void setUp() {
        def jobName = "dummy_job"
        def testManifest = "tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml"
        def buildId = 215
        def buildManifest = "tests/jenkins/data/opensearch-dashboards-1.2.0-build.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/1.2.0/${buildId}/linux/x64/tar/dist/opensearch-dashboards/opensearch-dashboards-1.2.0-linux-x64.tar.gz"
        def agentLabel = "Jenkins-Agent-al2-x64-c54xlarge-Docker-Host"

        this.registerLibTester(new DetectTestDockerAgentLibTester())
        this.registerLibTester(new DownloadBuildManifestLibTester(buildManifestUrl, buildManifest))
        this.registerLibTester(new RunIntegTestScriptLibTester(jobName, buildManifest, "manifests/${testManifest}", "${buildId}"))
        this.registerLibTester(new UploadTestResultsLibTester(buildManifest, jobName, buildId))
        this.registerLibTester(new PublishNotificationLibTester(
                ':white_check_mark:',
                'Integration Tests Successful',
                '',
                testManifest,
                'INTEG_TEST_WEBHOOK'))
        super.setUp()

        // Variables
        binding.setVariable('TEST_MANIFEST', testManifest)
        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('AGENT_LABEL', agentLabel)
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('BUILD_ID', "${buildId}")
        def env = binding.getVariable('env')
        env['DOCKER_AGENT'] = [image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11']
        
        binding.getVariable('currentBuild').upstreamBuilds = [[fullProjectName: jobName]]
        
        helper.registerAllowedMethod('fileExists', [String.class], { args ->
            return true;
        })

        helper.registerAllowedMethod('findFiles', [Map.class], null)
    }

    @Test
    void integTests_runs_consistently() {
        super.testPipeline('jenkins/opensearch-dashboards/integ-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch-dashboards/integ-test.jenkinsfile')
    }
}
