/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import org.junit.*
import com.lesfurets.jenkins.unit.*
import static org.assertj.core.api.Assertions.*

class TestHello extends BasePipelineTest {
    def jenkinsScript = "tests/jenkins/jobs/Hello_Jenkinsfile"

    @Override
    @Before
    void setUp() throws Exception {
        super.setUp()
    }

    @Test
    void testHello() {
        runScript(jenkinsScript)
        RegressionTestHelper.testNonRegression(helper, jenkinsScript)
        assertJobStatusSuccess()
        printCallStack()
    }
}
