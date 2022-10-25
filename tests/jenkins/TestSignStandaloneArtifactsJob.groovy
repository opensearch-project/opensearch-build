/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestSignStandaloneArtifactsJob extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        def filenamesForUrls = ['dummy_1_artifact.tar.gz', 'dummy_1_artifact.tar.gz.sig',
                                'dummy_2_artifact.tar.gz', 'dummy_2_artifact.tar.gz.sig']

        def sigtype = '.sig'
        def platform = 'linux'
        def artifactPath = "${this.workspace}/artifacts"

        // this.registerLibTester(new SignArtifactsLibTester(sigtype, platform, artifactPath, null, null))
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        helper.registerAllowedMethod('git', [Map])
        helper.registerAllowedMethod('withCredentials', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        // this.registerLibTester(new PrintArtifactDownloadUrlsForStagingLibTester(filenamesForUrls, 'sign_artifacts_job/dummy/upload/path/20/dist/signed'))

        // this.registerLibTester(new UploadToS3LibTester(artifactPath, 'dummy_bucket_name', 'sign_artifacts_job/dummy/upload/path/20/dist/signed'))
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'dummy_bucket_name')
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })        

        super.setUp()

        // Params
        binding.setVariable('URLs', 'https://www.dummy.com/dummy_1_artifact.tar.gz,' +
                ' https://www.dummy.com/dummy_2_artifact.tar.gz')
        binding.setVariable('S3_FILE_UPLOAD_PATH', '/dummy/upload/path/')
        binding.setVariable('DISTRIBUTION_PLATFORM', platform)
        binding.setVariable('SIGNATURE_TYPE', sigtype)
    }

    @Test
    void testSignArtifactsJob() {

        binding.setVariable('JOB_NAME', 'sign_artifacts_job')
        binding.setVariable('BUILD_NUMBER', '20')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'dummy_bucket_name')

        super.testPipeline("jenkins/sign-artifacts/sign-standalone-artifacts.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/sign-standalone-artifacts/sign-standalone-artifacts.jenkinsfile")

    }

}
