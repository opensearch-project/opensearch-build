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


class TestCreateTestResultsMessage extends BuildPipelineTest {
    @Before
    void setUp() {
        this.registerLibTester(
            new CreateTestResultsMessageLibTester(
                'Integ Tests (x64)',
                'SUCCESS',
                'dummy-test.com/test-results'
            )
        )
        super.setUp()
    }

    @Test
    public void TestCreateTestResultsMessage() {
        super.testPipeline("tests/jenkins/jobs/CreateTestResultsMessage_Jenkinsfile")
    }
}
