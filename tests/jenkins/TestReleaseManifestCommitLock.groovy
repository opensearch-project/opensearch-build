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
        super.testPipeline('jenkins/release-workflows/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/testManifestCommitLock_matchBuildManifest')
        def callStack = helper.getCallStack()
        assertCallStack().contains('stage(Parameters Check, groovy.lang.Closure)')
        assertCallStack().contains('stage(MATCH_BUILD_MANIFEST, groovy.lang.Closure)')
    }

    @Test
    public void testManifestCommitLock_updateToRecentCommits() {
        addParam('MANIFEST_LOCK_ACTION', 'UPDATE_TO_RECENT_COMMITS')
        super.testPipeline('jenkins/release-workflows/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/testManifestCommitLock_updateToRecentCommits')
        def callStack = helper.getCallStack()
        assertCallStack().contains('stage(Parameters Check, groovy.lang.Closure)')
        assertCallStack().contains('stage(UPDATE_TO_RECENT_COMMITS, groovy.lang.Closure)')
    }

    @Test
    public void testManifestCommitLock_updateToTags() {
        addParam('MANIFEST_LOCK_ACTION', 'UPDATE_TO_TAGS')
        super.testPipeline('jenkins/release-workflows/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/testManifestCommitLock_updateToTags')
        def callStack = helper.getCallStack()
        assertCallStack().contains('stage(Parameters Check, groovy.lang.Closure)')
        assertCallStack().contains('stage(UPDATE_TO_TAGS, groovy.lang.Closure)')
        assertCallStack().contains('Skipping stage MATCH_BUILD_MANIFEST')
        assertCallStack().contains('Skipping stage UPDATE_TO_RECENT_COMMITS')
        assertCallStack().contains('release-manifest-commit-lock.writeYaml({file=manifests/2.0.0/opensearch-2.0.0.yml, data={schema-version=1.0, build={name=OpenSearch, version=2.0.0, qualifier=alpha1}, ci={image={name=opensearchstaging/ci-runner:ci-runner-centos7-opensearch-build-v2, args=-e JAVA_HOME=/opt/java/openjdk-17}}, components=[{name=OpenSearch, ref=tags/2.0.0, repository=https://github.com/opensearch-project/OpenSearch.git, checks=[gradle:publish, gradle:properties:version]}, {name=common-utils, repository=https://github.com/opensearch-project/common-utils.git, ref=2.0, checks=[gradle:publish, gradle:properties:version]}, {name=job-scheduler, repository=https://github.com/opensearch-project/job-scheduler.git, ref=2.0, checks=[gradle:properties:version, gradle:dependencies:opensearch.version]}]}, overwrite=true})')
    }

    @Test
    public void testManifestCommitLock_createPullRequest() {
        super.testPipeline('jenkins/release-workflows/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/testManifestCommitLock_createPullRequest')
        assertThat(getShellCommands('git'), hasItem("\n                                git remote set-url origin \"https://opensearch-ci:GITHUB_TOKEN@github.com/opensearch-project/opensearch-build\"\n                                git config user.email \"opensearch-infra@amazon.com\"\n                                git config user.name \"opensearch-ci\"\n                                git checkout -b manifest-lock\n                            "))
        assertThat(getShellCommands('git'), hasItem("\n                                    git status --porcelain | grep '^ M' | cut -d \" \" -f3 | xargs git add\n                                    git commit -sm \"Manifest Commit Lock for Release 2.0.0\"\n                                    git push origin manifest-lock --force\n                                    gh pr create --title '[2.0.0] Manifest Commit Lock with action MATCH_BUILD_MANIFEST' --body 'Manifest Commit Lock for Release 2.0.0 ' -H manifest-lock -B main\n                                "))
    }

    @Test
    public void testUpdateToRecentCommit() {
        addParam('MANIFEST_LOCK_ACTION', 'UPDATE_TO_RECENT_COMMITS')
        helper.addShMock("""git ls-remote https://github.com/opensearch-project/OpenSearch.git 2.0""") { script ->
            return [stdout: "", exitValue: 0]
        }
        super.testPipeline('jenkins/release-workflows/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/testUpdateToRecentCommit')
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
        super.testPipeline('jenkins/release-workflows/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/testMatchBuildManifest')
        assertThat(getShellCommands('curl'), hasItem("{script=curl -sSL https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0/3813/linux/x64/tar/dist/opensearch/manifest.yml, returnStdout=true}"))
        assertCallStack().contains("release-manifest-commit-lock.writeYaml({file=manifests/2.0.0/opensearch-dashboards-2.0.0.yml, data={schema-version=1.1, build={name=OpenSearch, version=2.0.0, platform=linux, architecture=x64, distribution=tar, location=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0/3813/linux/x64/tar/dist/opensearch/opensearch-2.0.0-linux-x64.tar.gz, id=3813}, components=[{name=OpenSearch, repository=https://github.com/opensearch-project/OpenSearch.git, ref=bae3b4e4178c20ac24fece8e82099abe3b2630d0, commit_id=bae3b4e4178c20ac24fece8e82099abe3b2630d0, location=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0/3813/linux/x64/tar/builds/opensearch/dist/opensearch-min-2.0.0-linux-x64.tar.gz}, {name=common-utils, repository=https://github.com/opensearch-project/common-utils.git, ref=2.0, commit_id=e59ea173af31fd468ce443fc4022649cad306e36}, {name=job-scheduler, repository=https://github.com/opensearch-project/job-scheduler.git, ref=2.0, commit_id=b5b21097894ecec7a78da622ee96763908b32898, location=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0/3813/linux/x64/tar/builds/opensearch/plugins/opensearch-job-scheduler-2.0.0.0.zip}, {name=ml-commons, repository=https://github.com/opensearch-project/ml-commons.git, ref=2.0, commit_id=5c6e4bd4d996cf2d0a9726e1537ef98822d1795f, location=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.0.0/3813/linux/x64/tar/builds/opensearch/plugins/opensearch-ml-2.0.0.0.zip}]}, overwrite=true})")
        assertCallStack().contains("release-manifest-commit-lock.writeYaml(")

    }

    @Test
    public void test_excludeFTRepo() {
        addParam('MANIFEST_LOCK_ACTION', 'UPDATE_TO_RECENT_COMMITS')
        def buildManifest = "tests/jenkins/data/opensearch-dashboards-3.0.0.yml"
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((buildManifest as File).text)
        }) 
        super.testPipeline('jenkins/release-workflows/release-manifest-commit-lock.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-workflows/testUpdateToRecentCommit_excludeFTRepo')
        // The test asserts that FT repo uses the release branch
        assertCallStack().contains("release-manifest-commit-lock.writeYaml({file=manifests/2.0.0/opensearch-dashboards-2.0.0.yml, data={ci={image={name=opensearchstaging/ci-runner:centos7-x64-arm64-jdkmulti-node10.24.1-cypress6.9.1-20211028}}, build={name=OpenSearch Dashboards, version=3.0.0}, components=[{name=OpenSearch-Dashboards, ref=tags/3.0.0, repository=https://github.com/opensearch-project/OpenSearch-Dashboards.git}, {name=functionalTestDashboards, repository=https://github.com/opensearch-project/opensearch-dashboards-functional-test.git, ref=3.0}, {name=observabilityDashboards, ref=tags/3.0.0, repository=https://github.com/opensearch-project/dashboards-observability.git}, {name=indexManagementDashboards, ref=tags/3.0.0, repository=https://github.com/opensearch-project/index-management-dashboards-plugin}, {name=ganttChartDashboards, ref=tags/3.0.0, repository=https://github.com/opensearch-project/dashboards-visualizations.git}, {name=reportsDashboards, ref=tags/3.0.0, repository=https://github.com/opensearch-project/dashboards-reports.git}, {name=queryWorkbenchDashboards, ref=tags/3.0.0, repository=https://github.com/opensearch-project/sql.git}, {name=anomalyDetectionDashboards, ref=tags/3.0.0, repository=https://github.com/opensearch-project/anomaly-detection-dashboards-plugin}], schema-version=1.0}, overwrite=true})")
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
