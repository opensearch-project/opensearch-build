/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestReleaseTagJob extends BuildPipelineTest {

    @Before
    void setUp() {

        def buildManifest = 'tests/data/opensearch-build-1.1.0.yml'

        this.registerLibTester(new CreateReleaseTagLibTester(buildManifest, '1.1.0'))

        super.setUp()

        // Variables for Release Tag Job
        binding.setVariable('VERSION', '1.1.0')
        binding.setVariable('BUILD_MANIFEST', buildManifest)

    }

    @Test
    void ReleaseTag_test() {
        super.testPipeline('jenkins/release-tag/release-tag.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-tag/release-tag.jenkinsfile')
    }
}
