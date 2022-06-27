/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestPublishNotification extends BuildPipelineTest {
    @Override
    @Before
    void setUp() {

        this.registerLibTester(new PublishNotificationLibTester(
                ':white_check_mark:', 'Successful Build' , 'extra', '1.2.0/opensearch-1.2.0.yml', 'jenkins-build-notice-webhook'))

        super.setUp()
    }

    @Test
    public void test() {
        super.testPipeline("tests/jenkins/jobs/PublishNotification_Jenkinsfile")
    }
}
