/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat
import static org.junit.jupiter.api.Assertions.assertThrows
import com.lesfurets.jenkins.unit.*
import groovy.json.JsonOutput

class TestReleaseManifestCommitLock extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('6.4.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()
        addParam('RELEASE_VERSION', '2.0.0')
        addParam('OPENSEARCH_RELEASE_CANDIDATE', '3813')
        addParam('OPENSEARCH_DASHBOARDS_RELEASE_CANDIDATE', '3050')
        addParam('COMPONENTS', 'OpenSearch')

        helper.registerAllowedMethod("withCredentials", [Map])
        def buildManifest = "tests/jenkins/data/opensearch-2.0.0.yml"
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((buildManifest as File).text)
        })
        helper.registerAllowedMethod("writeYaml", [Map.class], {c -> })
    }

    @Test
    public void testManifestCommitLock_matchBuildManifest() {
        addParam('MANIFEST_LOCK_ACTION', 'MATCH_BUILD_MANIFEST')
        super.testPipeline('jenkins/release-manifest-commit-lock/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-manifest-commit-lock/testManifestCommitLock_matchBuildManifest')
        def callStack = helper.getCallStack()
        assertCallStack().contains('stage(Parameters Check, groovy.lang.Closure)')
        assertCallStack().contains('stage(MATCH_BUILD_MANIFEST, groovy.lang.Closure)')
    }

    @Test
    public void testManifestCommitLock_updateToRecentCommits() {
        addParam('MANIFEST_LOCK_ACTION', 'UPDATE_TO_RECENT_COMMITS')
        super.testPipeline('jenkins/release-manifest-commit-lock/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-manifest-commit-lock/testManifestCommitLock_updateToRecentCommits')
        def callStack = helper.getCallStack()
        assertCallStack().contains('stage(Parameters Check, groovy.lang.Closure)')
        assertCallStack().contains('stage(UPDATE_TO_RECENT_COMMITS, groovy.lang.Closure)')
    }

    @Test
    public void testManifestCommitLock_createPullRequest() {
        super.testPipeline('jenkins/release-manifest-commit-lock/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-manifest-commit-lock/testManifestCommitLock_createPullRequest')
        assertThat(getShellCommands('git'), hasItem("\n                                git remote set-url origin \"https://opensearch-ci:GITHUB_TOKEN@github.com/opensearch-project/opensearch-build\"\n                                git config user.email \"opensearch-infra@amazon.com\"\n                                git config user.name \"opensearch-ci\"\n                                git checkout -b manifest-lock\n                            "))
        assertThat(getShellCommands('git'), hasItem("\n                                    git status --porcelain | grep '^ M' | cut -d \" \" -f3 | xargs git add\n                                    git commit -sm \"Manifest Commit Lock for Release 2.0.0\"\n                                    git push origin manifest-lock --force\n                                    gh pr create --title '[2.0.0] Manifest Commit Lock with action MATCH_BUILD_MANIFEST' --body 'Manifest Commit Lock for Release 2.0.0 ' -H manifest-lock -B main\n                                "))
    }

    @Test
    public void testUpdateToRecentCommit() {
        addParam('MANIFEST_LOCK_ACTION', 'UPDATE_TO_RECENT_COMMITS')
        helper.addShMock("""git ls-remote https://github.com/opensearch-project/OpenSearch.git 2.0""") { script ->
            return [stdout: "", exitValue: 0]
        }
        super.testPipeline('jenkins/release-manifest-commit-lock/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-manifest-commit-lock/testUpdateToRecentCommit')
        assertCallStack().contains('release-manifest-commit-lock.readYaml({file=manifests/2.0.0/opensearch-dashboards-2.0.0.yml})')
        assertCallStack().contains('release-manifest-commit-lock.readYaml({file=manifests/2.0.0/opensearch-dashboards-2.0.0.yml})')
        assertCallStack().contains('release-manifest-commit-lock.sh({script=git ls-remote https://github.com/opensearch-project/OpenSearch.git 2.0 | cut -f 1, returnStdout=true})')
        assertCallStack().contains("release-manifest-commit-lock.writeYaml({file=manifests/2.0.0/opensearch-2.0.0.yml")
        assertCallStack().contains("{name=common-utils, repository=https://github.com/opensearch-project/common-utils.git, ref=2.0, checks=[gradle:publish, gradle:properties:version]}, {name=job-scheduler, repository=https://github.com/opensearch-project/job-scheduler.git, ref=2.0, checks=[gradle:properties:version, gradle:dependencies:opensearch.version]}]}")
        assertCallStack().contains("release-manifest-commit-lock.readYaml({file=manifests/2.0.0/opensearch-dashboards-2.0.0.yml})")
    }

    @Test
    public void testMatchBuildManifest() {   
        addParam('MANIFEST_LOCK_ACTION', 'MATCH_BUILD_MANIFEST')
        def buildManifest = "tests/jenkins/data/opensearch-2.0.0-build.yml"
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((buildManifest as File).text)
        })     
        super.testPipeline('jenkins/release-manifest-commit-lock/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-manifest-commit-lock/testMatchBuildManifest')
        assertThat(getShellCommands('curl'), hasItem("{script=curl -sSL https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0/3813/linux/x64/tar/dist/opensearch/manifest.yml, returnStdout=true}"))
        assertCallStack().contains("release-manifest-commit-lock.writeYaml({file=manifests/2.0.0/opensearch-2.0.0.yml, data={schema-version=1.1, build={name=OpenSearch, version=2.0.0, platform=linux, architecture=x64, distribution=tar, location=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0/3813/linux/x64/tar/dist/opensearch/opensearch-2.0.0-linux-x64.tar.gz, id=3813}")
        assertCallStack().contains("release-manifest-commit-lock.writeYaml(")

    }

    def getShellCommands(searchtext) {
        def shCommands = helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.collect { call ->
            callArgsToString(call)
        }.findAll { gitCommand ->
            gitCommand.contains(searchtext)
        }
        return shCommands
    }
}
