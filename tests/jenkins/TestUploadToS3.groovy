import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestUploadToS3 extends BuildPipelineTest {

    static void setUpVariables(binding, helper){
        binding.setVariable('ARTIFACT_UPLOAD_ROLE_NAME', 'Dummy_Upload_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'dummy_bucket_name')
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    @Before
    void setUp() {
        super.setUp()
    }

    @Test
    void testSignArtifacts() {

        def sourcePath = '/tmp/src/path'
        def bucket = 'dummy_bucket'
        def path = '/upload/path'

        binding.setVariable('sourcePath', sourcePath)
        binding.setVariable('bucket', bucket)
        binding.setVariable('path', path)

        setUpVariables(binding, helper)

        super.testPipeline("tests/jenkins/jobs/UploadToS3_Jenkinsfile")

        verifyUploadToS3Params(helper, sourcePath, bucket, path)
    }

    static void verifyUploadToS3Params(helper, sourcePath, bucket, path) {
        assert helper.callStack.findAll { call ->
            call.methodName == 'uploadToS3'
        }.size() > 0

        helper.callStack.findAll { call ->
            call.methodName == 'uploadToS3'
        }.each { call ->
            assertThat(call.args.sourcePath.first(), notNullValue())
            assertThat(call.args.bucket.first(), notNullValue())
            assertThat(call.args.path.first(), notNullValue())
        }

        def callFound = false

        def callList = helper.callStack.findAll { call ->
            call.methodName == 'uploadToS3'
        }

        for(call in callList){
            if( call.args.sourcePath.first() == sourcePath
                    && call.args.bucket.first() == bucket
                    && call.args.path.first() == path){
                callFound = true
            }
        }

        assert callFound
    }
}
