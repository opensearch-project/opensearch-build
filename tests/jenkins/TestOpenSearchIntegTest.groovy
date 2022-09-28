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

class TestOpenSearchIntegTest extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        def jobName = "dummy_job"
        def testManifest = "tests/jenkins/data/opensearch-1.3.0-test.yml"
        def buildId = 717
        def buildManifest = "tests/jenkins/data/opensearch-1.3.0-build.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.0/${buildId}/linux/x64/dist/opensearch/opensearch-1.3.0-linux-x64.tar.gz"
        def agentLabel = "Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host"

        def destPath = "${this.workspace}/artifacts"
        def artifactsPath = "${jobName}/1.3.0/${buildId}/linux/x64/tar/"
        def bucketName = 'job-s3-bucket-name'

        this.registerLibTester(new DetectTestDockerAgentLibTester())
        this.registerLibTester(new DownloadFromS3LibTester(destPath, bucketName, artifactsPath, true))
        this.registerLibTester(new DownloadBuildManifestLibTester(buildManifestUrl, buildManifest))
        this.registerLibTester(new RunIntegTestScriptLibTester(jobName, 'OpenSearch', buildManifest, "manifests/${testManifest}", ''))
        this.registerLibTester(new UploadTestResultsLibTester(buildManifest, jobName))
        this.registerLibTester(new PublishNotificationLibTester(
                ':white_check_mark:',
                'Integration Tests Successful',
                '',
                testManifest,
                'jenkins-integ-test-webhook'))
        super.setUp()

        // Variables
        binding.setVariable('TEST_MANIFEST', testManifest)
        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('AGENT_LABEL', agentLabel)
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('BUILD_ID', "${buildId}")
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)
        def env = binding.getVariable('env')
        env['DOCKER_AGENT'] = [image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11']
        
        binding.getVariable('currentBuild').upstreamBuilds = [[fullProjectName: jobName]]
        
        helper.registerAllowedMethod('fileExists', [String.class], { args ->
            return true;
        })

        helper.registerAllowedMethod('findFiles', [Map.class], null)
        helper.registerAllowedMethod('unstash', [String.class], null)
        helper.registerAllowedMethod('fileExists', [String.class], { args ->
            return true;
        })

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.0.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
        )
    }

    @Test
    void integTests_runs_consistently() {
        super.testPipeline('jenkins/opensearch/integ-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch/integ-test.jenkinsfile')
    }
}
