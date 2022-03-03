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


class TestRunPerfTestScript extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new RunPerfTestScriptLibTester(
            'dummy_job',
            'tests/jenkins/data/opensearch-1.3.0-bundle.yml',
            '1236',
            'false',
            'nyc_taxis',
            '1',
            '1'
            )
        )
        super.setUp()
    }

    @Test
    public void TestRunPerfTestScript() {
        super.testPipeline("tests/jenkins/jobs/RunPerfTestScript_Jenkinsfile")
    }
}
