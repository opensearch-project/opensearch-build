/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

package jenkins.tests

import com.lesfurets.jenkins.unit.RegressionTestHelper
import com.lesfurets.jenkins.unit.declarative.DeclarativePipelineTest
import org.junit.Before

import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


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

    /**
     * The author of signArtifacts is responsible for this method.
     */
    void verifySignArtifacts() {
        def actualS3Upload = helper.callStack.findAll { call ->
            call.methodName == 'signArtifacts'
        }.each { call ->
            assertThat(call.args.signatureType, notNullValue())
            assertThat(call.args.signatureType.first(), anyOf(equalTo('.sig'), equalTo('.pgp')))
            assertThat(call.args.distributionPlatform, notNullValue())
            assertThat(call.args.distributionPlatform.first(), anyOf(equalTo('linux'), equalTo('macos')))
        }
    }
}
