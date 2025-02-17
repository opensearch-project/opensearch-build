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
import org.yaml.snakeyaml.Yaml

import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat

import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestReleaseChores extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('8.2.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()
    }

    @Test
    public void testVerifyParameters() {
        addParam('RELEASE_VERSION', '')
        addParam('RELEASE_CHORE', 'add_rc_details_comment')
        runScript('jenkins/release-workflows/release-chores.jenkinsfile')
        assertThat(getCommandExecutions('error', ''), hasItem('Required parameters are missing. Please provide the mandatory arguments RELEASE_VERSION and RELEASE_CHORE'))
    }

    def getCommandExecutions(methodName, command) {
        def shCommands = helper.callStack.findAll {
            call ->
                call.methodName == methodName
        }.
        collect {
            call ->
                callArgsToString(call)
        }.findAll {
            shCommand ->
                shCommand.contains(command)
        }
        return shCommands
    }
}
