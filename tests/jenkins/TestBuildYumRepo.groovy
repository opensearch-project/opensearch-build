/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
package jenkins.tests

import org.junit.*

class TestBuildYumRepo extends BuildPipelineTest {

    @Before
    void setUp() {
        this.registerLibTester(new BuildYumRepoTester(
            'tests/data/opensearch-build-1.3.0.yml',
            'https://ci.opensearch.org/ci/dbc/test/1.3.0/9/linux/x64'
        ))

        super.setUp()
    }

    @Test
    void testBuildYumRepo() {
        super.testPipeline('tests/jenkins/jobs/BuildYumRepo_Jenkinsfile')
    }

}
