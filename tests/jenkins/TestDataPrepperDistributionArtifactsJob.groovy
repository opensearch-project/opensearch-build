/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDataPrepperDistributionArtifactsJob extends BuildPipelineTest {

    @Before
    void setUp() {
        super.setUp()

        // job parameters
        def version = '0.22.1'
        def branch = 'refs/tags/0.22.1'

        // Variables for Data-prepper-Distribution-Artifacts-job
        def workspace = '/tmp/workspace'
        binding.setVariable('VERSION', version)
        binding.setVariable('BRANCH', branch)
        binding.setVariable('JOB_BASE_NAME', 'data-prepper-distribution-artifacts')
        binding.setVariable('BUILD_NUMBER', '51')
        binding.setVariable('WORKSPACE', '/tmp/workspace')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'job-s3-bucket-name')

        helper.registerAllowedMethod('checkout', [Map], {})

        def artifactsPath = "$workspace/release/archives/linux/build/distributions"
        helper.addShMock("find ${artifactsPath} | sed -n \"s|^${artifactsPath}/||p\"") { script ->
            return [stdout: "tar_dummy_1_artifact_1.0.0.tar.gz tar_dummy_2_artifact_1.0.0.tar.gz", exitValue: 0]
        }


        // Variables for signArtifacts library
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')

        binding.setVariable('SIGNER_CLIENT_ROLE', 'dummy_signer_client_role')
        binding.setVariable('SIGNER_CLIENT_EXTERNAL_ID', 'signer_client_external_id')
        binding.setVariable('SIGNER_CLIENT_UNSIGNED_BUCKET', 'signer_client_unsigned_bucket')
        binding.setVariable('SIGNER_CLIENT_SIGNED_BUCKET', 'signer_client_signed_bucket')

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("withCredentials", [Map])


        // Upload to s3
        binding.setVariable('ARTIFACT_UPLOAD_ROLE_NAME', 'Dummy_Upload_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'dummy_bucket_name')
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })


        // Post cleanup
        helper.registerAllowedMethod("cleanWs", [Map])
    }

    @Test
    void dataPrepperDistributionArtifacts_builds_consistently() {
        super.testPipeline('jenkins/data-prepper/distribution-artifacts.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/data-prepper/distribution-artifacts.jenkinsfile')
    }
}
