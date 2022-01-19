/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDataPrepperDistributionArtifacts extends BuildPipelineTest {

    public String artifactsPath

    @Before
    void setUp() {
        super.setUp()

        // Variables for Data-prepper-Distribution-Artifacts-job
        def workspace = '/tmp/workspace'
        binding.setVariable('VERSION', '0.22.1')
        binding.setVariable('BRANCH', 'refs/tags/0.22.1')
        binding.setVariable('JOB_BASE_NAME', 'data-prepper-distribution-artifacts')
        binding.setVariable('BUILD_NUMBER', '51')
        binding.setVariable('WORKSPACE', workspace)
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'job-s3-bucket-name')

        helper.registerAllowedMethod('checkout', [Map], {})

        artifactsPath = "$workspace/release/archives/linux/build/distributions"
        helper.addShMock("find ${artifactsPath} | sed -n \"s|^${artifactsPath}/||p\"") { script ->
            return [stdout: "tar_dummy_1_artifact_1.0.0.tar.gz tar_dummy_2_artifact_1.0.0.tar.gz", exitValue: 0]
        }

        // Variables for signArtifacts library
        TestSignArtifacts.setUpVariables(binding, helper)

        // Upload to s3
        TestUploadToS3.setUpVariables(binding, helper)
    }

    @Test
    void dataPrepperDistributionArtifacts_builds_consistently() {
        super.testPipeline('jenkins/data-prepper/distribution-artifacts.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/data-prepper/distribution-artifacts.jenkinsfile')

        TestSignArtifacts.verifySignArtifactsParams(helper, ".sig", "linux",
                "/tmp/workspace/release/archives/linux/build/distributions")

        def filenamesForUrls = ['tar_dummy_1_artifact_1.0.0.tar.gz', 'tar_dummy_1_artifact_1.0.0.tar.gz.sig',
                                'tar_dummy_2_artifact_1.0.0.tar.gz', 'tar_dummy_2_artifact_1.0.0.tar.gz.sig']
        TestPrintArtifactDownloadUrlsForStaging.verifyPrintArtifactDownloadUrlsForStagingParams(helper, filenamesForUrls,
                'data-prepper-distribution-artifacts/0.22.1/51/builds/signed')

        TestUploadToS3.verifyUploadToS3Params(helper, artifactsPath, 'dummy_bucket_name', 'data-prepper-distribution-artifacts/0.22.1/51/builds/signed')

    }
}
