/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import org.junit.*
import com.lesfurets.jenkins.unit.BasePipelineTest
import com.lesfurets.jenkins.unit.MethodCall
import static org.assertj.core.api.Assertions.assertThat

class TestHello extends BasePipelineTest {
    @Override
    @Before
    void setUp() throws Exception {
        super.setUp()
    }

    @Test
    void testHello() {
        runScript('tests/jenkins/jobs/Hello_Jenkinsfile')
        assertJobStatusSuccess()
        assertThat(helper.callStack.stream()
            .filter { c -> c.methodName == "echo"  }
            .map(MethodCall.&callArgsToString)
            .findAll { s -> s == "Hello World!" }
        ).hasSize(1)
        printCallStack()
    }
}
