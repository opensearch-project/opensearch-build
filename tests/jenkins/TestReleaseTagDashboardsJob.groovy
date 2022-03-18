/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestReleaseTagDashboardsJob extends BuildPipelineTest {

    @Before
    void setUp() {

        def distManifest = 'tests/data/opensearch-dashboards-build-1.2.0.yml'

        this.registerLibTester(new CreateReleaseTagLibTester(distManifest, '1.2.0'))

        super.setUp()

        // Variables for Release Tag Job
        binding.setVariable('VERSION', '1.2.0')
        binding.setVariable('PRODUCT', 'opensearch-dashboards')
        binding.setVariable('DISTRIBUTION_MANIFEST', distManifest)

    }

    @Test
    void ReleaseTagDashboards_test() {
        super.testPipeline('jenkins/release-tag/release-tag.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-tag/release-tag-dashboards.jenkinsfile')
    }
}
