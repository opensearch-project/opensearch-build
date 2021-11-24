/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*

class TestInputManifest extends BuildPipelineTest {
    @Test
    void testInputManifest() {
        super.testPipeline("tests/jenkins/jobs/InputManifest_Jenkinsfile")
    }
}
