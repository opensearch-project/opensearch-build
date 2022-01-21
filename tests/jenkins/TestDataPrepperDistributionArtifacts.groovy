/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDataPrepperDistributionArtifacts extends BuildPipelineTest {

    @Before
    void setUp() {

        def filenamesForUrls = ['tar_dummy_1_artifact_1.0.0.tar.gz', 'tar_dummy_1_artifact_1.0.0.tar.gz.sig',
                                'tar_dummy_2_artifact_1.0.0.tar.gz', 'tar_dummy_2_artifact_1.0.0.tar.gz.sig']

        def artifactsPath = "${this.workspace}/release/archives/linux/build/distributions"

        def bucketName = 'job-s3-bucket-name'

        this.registerLibTester(new TestUploadToS3(
                sourcePath: artifactsPath,
                bucket: bucketName,
                path: 'data-prepper-distribution-artifacts/0.22.1/51/builds/signed'
        ))

        this.registerLibTester(new TestSignArtifacts(
                signatureType: '.sig',
                distributionPlatform: 'linux',
                artifactPath: artifactsPath
        ))

        this.registerLibTester(new TestPrintArtifactDownloadUrlsForStaging(
                artifactFileNames: filenamesForUrls,
                uploadPath: 'data-prepper-distribution-artifacts/0.22.1/51/builds/signed'
        ))

        super.setUp()

        // Variables for Data-prepper-Distribution-Artifacts-job
        binding.setVariable('VERSION', '0.22.1')
        binding.setVariable('BRANCH', 'refs/tags/0.22.1')
        binding.setVariable('JOB_BASE_NAME', 'data-prepper-distribution-artifacts')
        binding.setVariable('BUILD_NUMBER', '51')
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)

        helper.registerAllowedMethod('checkout', [Map], {})

        helper.addShMock("find ${artifactsPath} | sed -n \"s|^${artifactsPath}/||p\"") { script ->
            return [stdout: "tar_dummy_1_artifact_1.0.0.tar.gz tar_dummy_2_artifact_1.0.0.tar.gz", exitValue: 0]
        }
    }

    @Test
    void dataPrepperDistributionArtifacts_builds_consistently() {
        super.testPipeline('jenkins/data-prepper/distribution-artifacts.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/data-prepper/distribution-artifacts.jenkinsfile')

    }
}
