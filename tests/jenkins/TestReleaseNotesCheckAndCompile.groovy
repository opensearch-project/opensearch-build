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

class TestReleaseNotesCheckAndCompile extends BuildPipelineTest {

    String gitLogDate = '2022-10-10'
    String comment = 'NO_COMMENT'
    String gitIssueNumber = '123456'
    String commentUniqueID = '123456'
    String releaseVersion = '3.0.0'

    @Override
    @Before
    void setUp() {

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

        addParam('RELEASE_VERSION', releaseVersion)
    }

    @Test
    public void releaseNotesCheck() {
        addParam('ACTION', 'check')
        addParam('GIT_LOG_DATE', gitLogDate)
        addParam('COMMENT', comment)
        addParam('GIT_ISSUE_NUMBER', gitIssueNumber)
        addParam('COMMENT_UNIQUE_ID', commentUniqueID)

        super.testPipeline("jenkins/release-workflows/release-notes-check.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/release-workflows/release-notes-check.jenkinsfile")
        assertJobStatusSuccess()
        def callStack = helper.getCallStack()
        assertCallStack().contains('Check release notes, groovy.lang.Closure')
        assertCallStack().contains('Skipping stage Generate consolidated release notes')
        assertThat(helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.any { call ->
            callArgsToString(call).contains('./release_notes.sh check manifests/3.0.0/opensearch-3.0.0.yml manifests/3.0.0/opensearch-dashboards-3.0.0.yml --date 2022-10-10')
        }).isTrue()    
    }

    @Test
    public void releaseNotesCompile() {
        addParam('ACTION', 'compile')
        super.testPipeline("jenkins/release-workflows/release-notes-check.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/release-workflows/release-notes-compile.jenkinsfile")
        assertJobStatusSuccess()
        def callStack = helper.getCallStack()
        assertCallStack().contains('Skipping stage Check release notes')
        assertCallStack().contains('Generate consolidated release notes, groovy.lang.Closure')
        assertThat(helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.any { call ->
            callArgsToString(call).contains('./release_notes.sh compile manifests/3.0.0/opensearch-3.0.0.yml manifests/3.0.0/opensearch-dashboards-3.0.0.yml --output opensearch-release-notes-3.0.0.md')
        }).isTrue()
    }
}