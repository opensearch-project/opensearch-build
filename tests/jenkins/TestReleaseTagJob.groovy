/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestReleaseTagJob extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        def distManifest = 'tests/data/opensearch-build-1.1.0.yml'

        this.registerLibTester(new CreateReleaseTagLibTester(distManifest, '1.1.0'))

        super.setUp()

        // Variables for Release Tag Job
        binding.setVariable('VERSION', '1.1.0')
        binding.setVariable('PRODUCT', 'opensearch')
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
    void ReleaseTag_test() {
        super.testPipeline('jenkins/release-tag/release-tag.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-tag/release-tag.jenkinsfile')
    }
}
