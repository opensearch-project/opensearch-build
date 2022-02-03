import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test


class TestUploadToS3 extends BuildPipelineTest {

    @Before
    void setUp() {

        this.registerLibTester(new UploadToS3LibTester( '/tmp/src/path', 'dummy_bucket', '/upload/path' ))

        super.setUp()
    }

    @Test
    void testUploadToS3() {
        super.testPipeline("tests/jenkins/jobs/UploadToS3_Jenkinsfile")
    }
}
