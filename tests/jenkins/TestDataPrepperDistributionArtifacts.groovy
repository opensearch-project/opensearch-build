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

        def dummyBuildArtifacts = "tar_dummy_1_artifact_1.0.0.tar.gz tar_dummy_2_artifact_1.0.0.tar.gz"

        def artifactsPath = "${this.workspace}/release/archives/linux/build/distributions"

        def filenamesForUrls = ['tar_dummy_1_artifact_1.0.0.tar.gz', 'tar_dummy_2_artifact_1.0.0.tar.gz',
                                            'tar_dummy_1_artifact_1.0.0.tar.gz.sig', 'tar_dummy_2_artifact_1.0.0.tar.gz.sig']

        def bucketName = 'job-s3-bucket-name'

        this.registerLibTester(new SignArtifactsLibTester( '.sig', 'linux',  artifactsPath, null, null))

        this.registerLibTester(new UploadToS3LibTester( artifactsPath, bucketName, 'data-prepper-distribution-artifacts/0.22.1/51/builds/signed'))

        this.registerLibTester(new PrintArtifactDownloadUrlsForStagingLibTester( filenamesForUrls, 'data-prepper-distribution-artifacts/0.22.1/51/builds/signed'))

        super.setUp()

        // Variables for Data-prepper-Distribution-Artifacts-job
        binding.setVariable('VERSION', '0.22.1')
        binding.setVariable('BRANCH', 'refs/tags/0.22.1')
        binding.setVariable('JOB_BASE_NAME', 'data-prepper-distribution-artifacts')
        binding.setVariable('BUILD_NUMBER', '51')
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)

        helper.registerAllowedMethod('checkout', [Map], {})

        helper.addShMock("find ${artifactsPath} | sed -n \"s|^${artifactsPath}/||p\"") { script ->
            return [stdout: dummyBuildArtifacts, exitValue: 0]
        }
    }

    @Test
    void dataPrepperDistributionArtifacts_builds_consistently() {
        super.testPipeline('jenkins/data-prepper/distribution-artifacts.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/data-prepper/distribution-artifacts.jenkinsfile')
    }
}
