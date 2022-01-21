import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestSignStandaloneArtifactsJob extends BuildPipelineTest {

    @Before
    void setUp() {

        def filenamesForUrls = ['dummy_1_artifact.tar.gz', 'dummy_1_artifact.tar.gz.sig',
                                'dummy_2_artifact.tar.gz', 'dummy_2_artifact.tar.gz.sig']

        def signatureType = '.sig'
        def distributionPlatform = 'linux'
        def artifactPath = "${this.workspace}/artifacts/"

        this.registerLibTester(new TestSignArtifacts(
                signatureType: signatureType,
                distributionPlatform: distributionPlatform,
                artifactPath: artifactPath
        ))

        this.registerLibTester(new TestPrintArtifactDownloadUrlsForStaging(
                artifactFileNames: filenamesForUrls,
                uploadPath: 'sign_artifacts_job/dummy/upload/path/20/dist/signed'
        ))

        super.setUp()

        binding.setVariable('DISTRIBUTION_PLATFORM', distributionPlatform)
        binding.setVariable('SIGNATURE_TYPE', signatureType)
        binding.setVariable('artifactPath', artifactPath)

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
                "tests/jenkins/jenkinsjob-regression-files/sign-standalone-artifacts/sign-standalone-artifacts.jenkinsfile")

    }

}
