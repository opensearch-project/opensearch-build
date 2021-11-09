/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import com.lesfurets.jenkins.unit.BasePipelineTest
import com.lesfurets.jenkins.unit.MethodCall
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.rules.ExpectedException
import static org.assertj.core.api.Assertions.assertThat

class TestHello extends BasePipelineTest {
    @Rule
    public ExpectedException thrown = ExpectedException.none()

    @Override
    @Before
    void setUp() throws Exception {
        scriptRoots += 'tests/jenkins/jobs'
        super.setUp()
    }

    @Test
    void testHello() {
        runScript("hello.groovy")
        assertJobStatusSuccess()
        assertThat(helper.callStack.stream()
            .filter { c -> c.methodName ==~ /echo/  }
            .map(MethodCall.&callArgsToString)
            .findAll { s -> s =~ /Hello.*/ })
            .hasSize(1)
        printCallStack()
    }
}
