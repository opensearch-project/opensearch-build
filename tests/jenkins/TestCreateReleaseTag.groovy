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

class TestCreateReleaseTag extends BuildPipelineTest {

    @Before
    void setUp() {

        this.registerLibTester(new CreateReleaseTagLibTester('tests/data/opensearch-build-1.1.0.yml', '1.1.0'))
        super.setUp()

    }

    @Test
    void testCreateReleaseTag() {
        super.testPipeline("tests/jenkins/jobs/CreateReleaseTag_Jenkinsfile")
    }
}
