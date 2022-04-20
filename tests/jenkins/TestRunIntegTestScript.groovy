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


class TestRunIntegTestScript extends BuildPipelineTest {

    @Test
    public void TestRunIntegTestScript() {
        this.registerLibTester(new RunIntegTestScriptLibTester(
            'dummy_job',
            'tests/jenkins/data/opensearch-1.3.0-build.yml',
            'tests/jenkins/data/opensearch-1.3.0-test.yml',
            '717'
            )
        )

        super.testPipeline("tests/jenkins/jobs/RunIntegTestScript_Jenkinsfile")
    }

    @Test
    public void TestRunIntegTestScript_OpenSearch_Dashboards() {
        this.registerLibTester(new RunIntegTestScriptLibTester(
            'dummy_job',
            'tests/jenkins/data/opensearch-dashboards-1.2.0-build.yml',
            'tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml',
            '215'
            )
        )

        super.testPipeline("tests/jenkins/jobs/RunIntegTestScript_OpenSearch_Dashboards_Jenkinsfile")
    }
}
