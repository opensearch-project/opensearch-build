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


class TestBuildInfoYaml extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new BuildInfoYamlLibTester(
                '',
                'tests/jenkins/data/opensearch-2.2.0.yml',
                'tests/jenkins/data/buildInfo.yml',
                'NOT_STARTED',
                'INITIALIZE_STAGE'
            )
        )
        super.setUp()
    }

    @Test
    void testBuildInfoYaml() {
        super.testPipeline("tests/jenkins/jobs/BuildInfoYaml_Jenkinsfile")
    }
}
