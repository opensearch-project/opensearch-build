/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import org.yaml.snakeyaml.Yaml
import jenkins.BundleManifest

class TestReleaseTagDashboardsJob extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        def tagVersion = '2.0.0-rc1'
        def distManifest = 'tests/jenkins/data/opensearch-dashboards-bundle-2.0.0-rc1.yml'

    //    this.registerLibTester(new CreateReleaseTagLibTester(distManifest, '2.0.0-rc1'))
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'dummy_token_name')
        binding.setVariable('GITHUB_USER', 'dummy_user')
        binding.setVariable('GITHUB_TOKEN', 'dummy_token')

        helper.registerAllowedMethod("checkout", [Map], {})
        helper.registerAllowedMethod("dir", [Map], {})
        InputStream inputStream = new FileInputStream(new File(distManifest));
        Yaml yaml = new Yaml()
        Map ymlMap = yaml.load(inputStream)
        BundleManifest bundleManifestObj = new BundleManifest(ymlMap)
        ArrayList bundleManifestComponentsList = bundleManifestObj.getNames()
        boolean checkFirst = true
        for (component in bundleManifestComponentsList) {
            def repo = bundleManifestObj.getRepo(component)
            def version = tagVersion
            if (tagVersion.contains("-")) {
                version = tagVersion.split("-").first() + ".0-" + tagVersion.split("-").last()
            } else {
                version = "$tagVersion.0"
            }
            if (component == "OpenSearch" || component == "OpenSearch-Dashboards" || component == "functionalTestDashboards") {
                version = tagVersion
            }
            def out = ""
            if (checkFirst) {
                out = bundleManifestObj.getCommitId(component)
                checkFirst = false
            }
            helper.addShMock("git ls-remote --tags $repo $version | awk 'NR==1{print \$1}'") { script ->
                return [stdout: out, exitValue: 0]
            }
        }

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
