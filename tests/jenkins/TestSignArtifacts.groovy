/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.*
import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestSignArtifacts extends BuildPipelineTest {

    static void setUpVariables(binding, helper){
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        binding.setVariable('SIGNER_CLIENT_ROLE', 'dummy_signer_client_role')
        binding.setVariable('SIGNER_CLIENT_EXTERNAL_ID', 'signer_client_external_id')
        binding.setVariable('SIGNER_CLIENT_UNSIGNED_BUCKET', 'signer_client_unsigned_bucket')
        binding.setVariable('SIGNER_CLIENT_SIGNED_BUCKET', 'signer_client_signed_bucket')

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("withCredentials", [Map])
    }

    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('WORKSPACE', 'workspace')
        binding.setVariable('DISTRIBUTION_PLATFORM', 'linux')
        binding.setVariable('SIGNATURE_TYPE', '.sig')
        binding.setVariable('artifactPath', 'artifacts/')

        setUpVariables(binding, helper)

    }

    @Test
    void testSignArtifacts() {
        super.testPipeline("tests/jenkins/jobs/SignArtifacts_Jenkinsfile")
    }

    @Test
    void testSignArtifactsJob() {
        binding.setVariable('URLs', 'https://www.dummy.com/dummy_1_artifact.tar.gz,' +
                ' https://www.dummy.com/dummy_2_artifact.tar.gz')
        binding.setVariable('S3_FILE_UPLOAD_PATH', '/dummy/upload/path/')
        binding.setVariable('JOB_NAME', 'sign_artifacts_job')
        binding.setVariable('BUILD_NUMBER', '20')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('ARTIFACT_UPLOAD_ROLE_NAME', 'Dummy_Upload_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'dummy_bucket_name')

        helper.registerAllowedMethod("cleanWs", [Map])
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        super.testPipeline("jenkins/sign-artifacts/sign-standalone-artifacts.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/sign-standalone-artifacts.jenkinsfile")

        verifySignArtifactsParams(helper, '.sig', 'linux', 'workspace/artifacts/')


        def filenamesForUrls = ['dummy_1_artifact.tar.gz', 'dummy_1_artifact.tar.gz.sig',
                                'dummy_2_artifact.tar.gz', 'dummy_2_artifact.tar.gz.sig']
        TestPrintArtifactDownloadUrlsForStaging.verifyPrintArtifactDownloadUrlsForStagingParams(helper, filenamesForUrls,
                'sign_artifacts_job/dummy/upload/path/20/dist/signed')
    }

    static void verifySignArtifactsParams(helper, signatureType, distributionPlatform, artifactPath) {
        assert helper.callStack.findAll { call ->
            call.methodName == 'signArtifacts'
        }.size() > 0

        helper.callStack.findAll { call ->
            call.methodName == 'signArtifacts'
        }.each { call ->
            assertThat(call.args.signatureType, notNullValue())
            assertThat(call.args.signatureType.first(), anyOf(equalTo('.sig'), equalTo('.pgp')))
            assertThat(call.args.distributionPlatform, notNullValue())
            assertThat(call.args.distributionPlatform.first(), anyOf(equalTo('linux')))
            assertThat(call.args.artifactPath, notNullValue())
            assert call.args.signatureType.first() == signatureType
            assert call.args.distributionPlatform.first() == distributionPlatform
            assert call.args.artifactPath.first() == artifactPath
        }
    }
}
