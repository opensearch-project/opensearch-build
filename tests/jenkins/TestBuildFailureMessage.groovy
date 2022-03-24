package jenkins.tests

import org.junit.*
import com.lesfurets.jenkins.unit.*
import static groovy.test.GroovyAssert.*

class TestBuildFailureMessage extends BasePipelineTest {

    def buildFailureMessage

    @Before
    void setUp() {
        super.setUp()
        buildFailureMessage = loadScript("../../vars/buildFailureMessage.groovy")
    }

    @Test
    void testCall() {
        def result = buildFailureMessage()
        assertEquals "result:", result
    }


}
