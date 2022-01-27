/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestMavenSignReleaseJob extends BuildPipelineTest {

    @Before
    void setUp() {

        def localPath = "${this.workspace}/artifacts"

        def artifactsPath = "${this.workspace}/artifacts/distribution-build-opensearch/1.0.0/123/linux/x64/builds/opensearch/manifest.yml"

        def bucketPath = 'distribution-build-opensearch/1.0.0/123/linux/x64/builds'

        def bucketName = 'job-s3-bucket-name'

        this.registerLibTester(new DownloadFromS3LibTester(localPath, bucketName, 'distribution-build-opensearch/1.0.0/123/linux/x64/builds/', true))

        this.registerLibTester(new SignArtifactsLibTester( '.sig', 'linux',  artifactsPath, 'maven', null))

        super.setUp()

        // Variables for Data-prepper-Distribution-Artifacts-job
        binding.setVariable('VERSION', '1.0.0')
        binding.setVariable('BUILD_ID', '123')
        binding.setVariable('ARTIFACT_PATH', 'distribution-build-opensearch/1.0.0/123/linux/x64/builds')
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)
        binding.setVariable('SONATYPE_STAGING_PROFILE_ID', 'dummy_id')

        
        helper.registerAllowedMethod('checkout', [Map], {})

    }

    @Test
    void MavenSignRelease_test() {
        super.testPipeline('jenkins/opensearch_maven_release/maven-sign-release.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/maven-sign-release/maven-sign-release.jenkinsfile')
    }
}
