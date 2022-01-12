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

class TestRunIntegTests extends BuildPipelineTest {
    @Before
    void setUp() {
        super.setUp()
        binding.setVariable('BUILD_NUMBER', '33')
        helper.registerAllowedMethod("git", [Map])
    }

    @Test
    public void testBuilds_x64() {
        super.testPipeline(
            "tests/jenkins/jobs/RunIntegTests_x64_Jenkinsfile",
        )
    }

    @Test
    public void testBuilds_arm64() {
        super.testPipeline(
            "tests/jenkins/jobs/RunIntegTests_arm64_Jenkinsfile",
        )
    }
}
