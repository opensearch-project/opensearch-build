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

class TestBuildDockerImage extends BuildPipelineTest {
    @Override
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('BUILD_NUMBER', '33')

        helper.registerAllowedMethod("git", [Map])
    }

    @Test
    public void testSkipsBoth() {
        super.testPipeline(
            "tests/jenkins/jobs/BuildDockerImage_Jenkinsfile",
            "tests/jenkins/jobs/BuildDockerImage_Jenkinsfile_skips_both"
        )
    }

    @Test
    public void testBuildsBoth() {
        binding.env.ARTIFACT_URL_linux_x64 = 'opensearch.linux.x64'
        binding.env.ARTIFACT_URL_linux_arm64 = 'opensearch.linux.arm64'

        super.testPipeline(
            "tests/jenkins/jobs/BuildDockerImage_Jenkinsfile",
            "tests/jenkins/jobs/BuildDockerImage_Jenkinsfile_builds_both"
        )
    }

    @Test
    public void testSkipsMissing_x64() {
        binding.env.ARTIFACT_URL_linux_arm64 = 'opensearch.linux.arm64'

        super.testPipeline(
            "tests/jenkins/jobs/BuildDockerImage_Jenkinsfile",
            "tests/jenkins/jobs/BuildDockerImage_Jenkinsfile_skips_x64"
        )
    }

    @Test
    public void testSkipsMissing_arm64() {
        binding.env.ARTIFACT_URL_linux_x64 = 'opensearch.linux.x64'

        super.testPipeline(
            "tests/jenkins/jobs/BuildDockerImage_Jenkinsfile",
            "tests/jenkins/jobs/BuildDockerImage_Jenkinsfile_skips_arm64"
        )
    }
}
