/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

package jenkins.tests

import com.lesfurets.jenkins.unit.RegressionTestHelper
import com.lesfurets.jenkins.unit.declarative.DeclarativePipelineTest
import org.junit.Before


/**
 * This base test class holds common functions, but does not perform
 * any additional setup. Test authors can extend from this class if
 * they don't need common setup. Otherwise, please see the sub-classes.
 */
abstract class CommonPipelineTest extends DeclarativePipelineTest {
    @Override
    @Before
    void setUp() {
        super.setUp()
    }

    void testPipeline(String jenkinsScript, String regressionFilename = null) {
        runScript(jenkinsScript)
        RegressionTestHelper.testNonRegression(helper, regressionFilename ?: jenkinsScript)
        assertJobStatusSuccess()
        printCallStack()
    }
}
