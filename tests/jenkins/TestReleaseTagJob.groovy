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
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.assertj.core.api.Assertions.assertThat
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.CoreMatchers.hasItems
import org.yaml.snakeyaml.Yaml


class TestReleaseTag extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        String releaseVersion = '2.16.0'

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.0.4')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        super.setUp()
        addParam('VERSION', releaseVersion)
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        binding.setVariable('env', [
            'VERSION': releaseVersion,
            'OS_DISTRIBUTION_MANIFEST': 'opensearch-2.16.0/manifest.yml',
            'OSD_DISTRIBUTION_MANIFEST': 'opensearch-dashboards-2.16.0/manifest.yml'
            ])
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            if (args.file == 'opensearch-2.16.0/manifest.yml') {
                return new Yaml().load(('tests/jenkins/data/opensearch-dist-2.16.0.yml' as File).text)
            } else if (args.file == 'opensearch-dashboards-2.16.0/manifest.yml') {
                return new Yaml().load(('tests/jenkins/data/opensearch-dashboards-dist-2.16.0.yml' as File).text)
            }
        })
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/security.git 2.16.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: '30760168263404e628a25fd13a54100d2610810c', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/job-scheduler.git 2.16.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: 'b36f79336db82fd45db5665a5ac2e9368f0a1cdf', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/k-NN.git 2.16.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: 'c8ec49f1e2c9603498ca679727a499dc0b296e26', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/common-utils.git 2.16.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: 'cbc06a5eafe0009edbb2c865d7cd30262d04e502', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/OpenSearch.git 2.16.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: 'f84a26e76807ea67a69822c37b1a1d89e7177d9b', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/dashboards-visualizations.git 2.16.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: '5e86965658791648fad9d0fc573e470c59cce674', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/OpenSearch-Dashboards.git 2.16.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: '4b8826e7ffa6562825ca8aad676a8d89983c2d70', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/opensearch-dashboards-functional-test.git 2.16.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: '7c5e0482b844828cf2aec3b63841bd5d336d5668', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/dashboards-reporting.git 2.16.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: '49057e4f82b0390dc28d0e08009ec5f892d7af1a', exitValue: 0]
        }
        helper.addShMock("git ls-remote --tags https://github.com/opensearch-project/dashboards-observability.git 2.16.0.0 | awk 'NR==1{print \$1}'") { script ->
            return [stdout: '24d368e882ec01ff98e556725b84e332d4ab825e', exitValue: 0]
        }
    }
    @Test
    public void checkTagCreation() {
        super.testPipeline("jenkins/release-workflows/release-tag.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/release-workflows/release-tag.jenkinsfile")
        assertJobStatusSuccess()
    }

    @Test
    public void testManifestLock(){
        runScript('jenkins/release-workflows/release-tag.jenkinsfile')
        assertCallStack().contains('release-tag.stage(Lock Manifests to tags, groovy.lang.Closure',
        'release-tag.string({name=RELEASE_VERSION, value=2.16.0})',
        'release-tag.string({name=MANIFEST_LOCK_ACTION, value=UPDATE_TO_TAGS})',
        'release-tag.build({job=release-manifest-commit-lock, wait=true, parameters=[null, null]})')
    }
}