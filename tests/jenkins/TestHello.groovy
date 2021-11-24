/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*

class TestHello extends BuildPipelineTest {
    @Test
    void testHello() {
        super.testPipeline("tests/jenkins/jobs/Hello_Jenkinsfile")
    }
}
