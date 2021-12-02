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

class TestDetectDockerImage extends BuildPipelineTest {
    @Test
    public void test() {
        helper.registerAllowedMethod("git", [Map])

        super.testPipeline("tests/jenkins/jobs/DetectDockerImage_Jenkinsfile")
    }
}
