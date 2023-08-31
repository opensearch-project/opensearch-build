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

class TestReleaseNotesCheck extends BuildPipelineTest {

    String gitLogDate = '2022-10-10'
    String comment = 'NO_COMMENT'
    String gitIssueNumber = '123456'
    String commentUniqueID = '123456'
    String inputManifest = '3.0.0/opensearch-3.0.0.yml'

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

        binding.setVariable('INPUT_MANIFEST', inputManifest)
        binding.setVariable('GIT_LOG_DATE', gitLogDate)
        binding.setVariable('COMMENT', comment)
        binding.setVariable('GIT_ISSUE_NUMBER', gitIssueNumber)
        binding.setVariable('COMMENT_UNIQUE_ID', commentUniqueID)
        binding.setVariable('AGENT_X64','Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host')
        binding.setVariable('dockerAgent', [image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11'])

    }

    @Test
    public void testReleaseNoteCheckPipeline() {
        super.testPipeline("jenkins/release-notes-check/release-notes-check.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/release-notes-check/release-notes-check.jenkinsfile")
    }

    @Test
    public void releaseNoteExecuteWithoutErrors() {
        runScript("jenkins/release-notes-check/release-notes-check.jenkinsfile")

        assertJobStatusSuccess()

        assertThat(helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.any { call ->
            callArgsToString(call).contains('release_notes.sh')
        }).isTrue()
    }
}