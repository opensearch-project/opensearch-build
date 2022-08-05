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


class TestGetRepositoryCommit extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new GetRepositoryCommitLibTester(
            '',
            'tests/jenkins/data/opensearch-2.0.0.yml',
            'commits.yml'
            )
        )
        super.setUp()
    }

    @Test
    void testGetRepositoryCommit() {
        super.testPipeline("tests/jenkins/jobs/GetRepositoryCommit_Jenkinsfile")
    }
}
