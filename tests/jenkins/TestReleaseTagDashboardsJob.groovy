/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestReleaseTagDashboardsJob extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        def distManifest = 'tests/jenkins/data/opensearch-dashboards-bundle-2.0.0-rc1.yml'

        this.registerLibTester(new CreateReleaseTagLibTester(distManifest, '2.0.0-rc1'))

        super.setUp()

        // Variables for Release Tag Job
        binding.setVariable('VERSION', '2.0.0-rc1')
        binding.setVariable('PRODUCT', 'opensearch-dashboards')
        binding.setVariable('DISTRIBUTION_MANIFEST', distManifest)

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.0.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
        )

    }

    @Test
    void ReleaseTagDashboards_test() {
        super.testPipeline('jenkins/release-tag/release-tag.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-tag/release-tag-dashboards.jenkinsfile')
    }
}
