/*
 * Copyright OpenSearch Contributors
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
            'OpenSearch',
            'tests/jenkins/data/opensearch-1.3.0-build.yml',
            'tests/jenkins/data/opensearch-1.3.0-test.yml',
            '',
            )
        )

        super.testPipeline("tests/jenkins/jobs/RunIntegTestScript_Jenkinsfile")
    }

    @Test
    public void TestRunIntegTestScript_OpenSearch_Dashboards() {
        this.registerLibTester(new RunIntegTestScriptLibTester(
            'dummy_job',
            'functionalTestDashboards',
            'tests/jenkins/data/opensearch-dashboards-1.2.0-build.yml',
            'tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml',
            '',
            )
        )

        super.testPipeline("tests/jenkins/jobs/RunIntegTestScript_OpenSearch_Dashboards_Jenkinsfile")
    }

    @Test
    public void TestRunIntegTestScript_LocalPath() {
        this.registerLibTester(new RunIntegTestScriptLibTester(
            'dummy_job',
            'OpenSearch',
            'tests/jenkins/data/opensearch-1.3.0-build.yml',
            'tests/jenkins/data/opensearch-1.3.0-test.yml',
            'tests/jenkins/artifacts/tar',
            )
        )

        super.testPipeline("tests/jenkins/jobs/RunIntegTestScript_LocalPath_Jenkinsfile")
    }
}
