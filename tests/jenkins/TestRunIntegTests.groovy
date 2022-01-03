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
    public void testSkipsMissing_x64() {
        super.testPipeline(
            "tests/jenkins/jobs/RunIntegTests_x64_Jenkinsfile",
            "tests/jenkins/jobs/RunIntegTests_x64_Jenkinsfile_skips_x64"
        )
    }

    @Test
    public void testSkipsMissing_arm64() {
        super.testPipeline(
            "tests/jenkins/jobs/RunIntegTests_arm64_Jenkinsfile",
            "tests/jenkins/jobs/RunIntegTests_arm64_Jenkinsfile_skips_arm64"
        )
    }

    @Test
    public void testBuilds_x64() {
        binding.env.ARTIFACT_URL_linux_x64 = 'opensearch.linux.x64'
        super.testPipeline(
            "tests/jenkins/jobs/RunIntegTests_x64_Jenkinsfile",
        )
    }

    @Test
    public void testBuilds_arm64() {
        binding.env.ARTIFACT_URL_linux_arm64 = 'opensearch.linux.arm64'
        super.testPipeline(
            "tests/jenkins/jobs/RunIntegTests_arm64_Jenkinsfile",
        )
    }
}
