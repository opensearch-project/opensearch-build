/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test


class TestRunBwcTestScript extends BuildPipelineTest {

    @Test
    public void TestRunBwcTestScript() {
        this.registerLibTester(new RunBwcTestScriptLibTester(
            'dummy_job',
            'tests/jenkins/data/opensearch-1.3.0-build.yml',
            'tests/jenkins/data/opensearch-1.3.0-test.yml',
            '717'
            )
        )

        super.testPipeline("tests/jenkins/jobs/RunBwcTestScript_Jenkinsfile")
    }

    @Test
    public void TestRunBwcTestScript_OpenSearch_Dashboards() {
        this.registerLibTester(new RunBwcTestScriptLibTester(
            'dummy_job',
            'tests/jenkins/data/opensearch-dashboards-1.2.0-build.yml',
            'tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml',
            '215'
            )
        )

        super.testPipeline("tests/jenkins/jobs/RunBwcTestScript_OpenSearch_Dashboards_Jenkinsfile")
    }
}
