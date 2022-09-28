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


class TestRunGradleCheck extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new RunGradleCheckLibTester(
            'https://github.com/opensearch-project/OpenSearch',
            'main',
            )
        )
        super.setUp()
    }

    @Test
    void testRunGradleCheck() {
        super.testPipeline("tests/jenkins/jobs/RunGradleCheck_Jenkinsfile")
    }
}
