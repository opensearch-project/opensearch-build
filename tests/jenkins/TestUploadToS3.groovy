import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestUploadToS3 extends BuildPipelineTest {

    private String sourcePath
    private String bucket
    private String path

    public LibTester libTester = new LibTester()

    @Before
    void setUp() {

        this.registerLibTester(new TestUploadToS3(
                sourcePath: '/tmp/src/path',
                bucket: 'dummy_bucket',
                path: '/upload/path'
        ).libTester)

        super.setUp()
    }

    @Test
    void testUploadToS3() {
        super.testPipeline("tests/jenkins/jobs/UploadToS3_Jenkinsfile")
    }

    class LibTester extends LibFunctionTester {

        void parameterInvariantsAssertions(call){
            assertThat(call.args.sourcePath.first(), notNullValue())
            assertThat(call.args.bucket.first(), notNullValue())
            assertThat(call.args.path.first(), notNullValue())
        }

        boolean expectedParametersMatcher(call) {
            return call.args.sourcePath.first() == sourcePath
                    && call.args.bucket.first() == bucket
                    && call.args.path.first() == path
        }

        String libFunctionName(){
            return 'uploadToS3'
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
    }
}
