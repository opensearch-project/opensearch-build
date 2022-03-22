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

    RunPerfTestScriptLibTester perfTestScriptLibTester

    @Before
    void setUp() {
        perfTestScriptLibTester = new RunPerfTestScriptLibTester(
            'tests/jenkins/data/opensearch-1.3.0-bundle.yml',
            '1236',
            'false',
            'nyc_taxis',
            '1',
            '1'
            )
        this.registerLibTester(perfTestScriptLibTester)
        super.setUp()
    }

    @Test
    public void TestRunPerfTestScript() {
        super.testPipeline("tests/jenkins/jobs/RunPerfTestScript_Jenkinsfile")
        perfTestScriptLibTester.setBundleManifest('tests/jenkins/data/opensearch-1.3.0-non-security-bundle.yml')
        super.testPipeline("tests/jenkins/jobs/RunPerfTestScriptWithoutSecurity_Jenkinsfile")
    }
}
