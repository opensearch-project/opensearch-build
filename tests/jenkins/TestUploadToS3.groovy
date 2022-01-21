import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestUploadToS3 extends BuildPipelineTest implements LibFunctionTester{

    private String sourcePath
    private String bucket
    private String path

    @Before
    void setUp() {

        this.sourcePath = '/tmp/src/path'
        this.bucket = 'dummy_bucket'
        this.path = '/upload/path'

        this.registerLibTester(new TestUploadToS3(
                sourcePath: sourcePath,
                bucket: bucket,
                path: path
        ))

        super.setUp()
    }

    @Test
    void testSignArtifacts() {

        binding.setVariable('sourcePath', sourcePath)
        binding.setVariable('bucket', bucket)
        binding.setVariable('path', path)

        super.testPipeline("tests/jenkins/jobs/UploadToS3_Jenkinsfile")

    }

    void configure(helper, binding){
        binding.setVariable('ARTIFACT_UPLOAD_ROLE_NAME', 'Dummy_Upload_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'dummy_bucket_name')
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    void verifyParams(helper) {
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
            if( call.args.sourcePath.first() == this.sourcePath
                    && call.args.bucket.first() == this.bucket
                    && call.args.path.first() == this.path){
                callFound = true
            }
        }

        assert callFound
    }
}
