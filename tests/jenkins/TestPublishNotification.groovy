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

class TestPublishNotification extends BuildPipelineTest {
    @Override
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('JOB_NAME', 'get-manifest-sha-build')
        binding.setVariable('BUILD_NUMBER', '33')
        binding.setVariable('BUILD_URL', 'http://jenkins.us-east-1.elb.amazonaws.com/job/vars/42')

        helper.registerAllowedMethod("git", [Map])
    }

    @Test
    public void test() {
        super.testPipeline("tests/jenkins/jobs/PublishNotification_Jenkinsfile")
    }
}
