/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import java.util.*

class TestMessages extends BuildPipelineTest {
    @Override
    @Before
    void setUp() {
        super.setUp()

        helper.registerAllowedMethod('findFiles', [Map.class], null)       
    }

    @Test
    public void testMessages() {
        super.testPipeline("tests/jenkins/jobs/Messages_Jenkinsfile")
    }
}
