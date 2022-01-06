/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import java.util.*
import java.nio.file.*

class TestSignArtifacts extends BuildPipelineTest {

    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('URLs', 'https://www.dummy.com/dummy_1_artifact.tar.gz,' +
                ' https://www.dummy.com/dummy_2_artifact.tar.gz')
        binding.setVariable('S3_FILE_UPLOAD_PATH', '/dummy/upload/path/')
        binding.setVariable('JOB_NAME', 'sign_artifacts_job')
        binding.setVariable('BUILD_NUMBER', '20')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('ARTIFACT_UPLOAD_ROLE_NAME', 'Dummy_Upload_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'dummy_bucket_name')
        binding.setVariable('DISTRIBUTION_PLATFORM', 'linux')
        binding.setVariable('SIGNATURE_TYPE', '.sig')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        binding.setVariable('WORKSPACE', 'workspace')

        binding.setVariable('SIGNER_CLIENT_ROLE', 'dummy_signer_client_role')
        binding.setVariable('SIGNER_CLIENT_EXTERNAL_ID', 'signer_client_external_id')
        binding.setVariable('SIGNER_CLIENT_UNSIGNED_BUCKET', 'signer_client_unsigned_bucket')
        binding.setVariable('SIGNER_CLIENT_SIGNED_BUCKET', 'signer_client_signed_bucket')

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    @Test
    void testSignArtifacts() {
        super.testPipeline("tests/jenkins/jobs/SignArtifacts_Jenkinsfile")
    }
}
