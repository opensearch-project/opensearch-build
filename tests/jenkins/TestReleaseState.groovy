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
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.CoreMatchers.containsString
import static org.hamcrest.MatcherAssert.assertThat
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestReleaseState extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('13.8.2')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withSecrets", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('writeFile', [Map])
        helper.registerAllowedMethod('groovyScript', [Map])
        helper.registerAllowedMethod('activeChoice', [Map.class], null)
        helper.registerAllowedMethod('stash', [Map])
        helper.registerAllowedMethod('unstash', [String])
        helper.registerAllowedMethod('writeJSON', [Map])
        helper.registerAllowedMethod('readJSON', [Map])
        binding.setVariable('METRICS_HOST_ACCOUNT', 'METRICS_HOST_ACCOUNT')
        binding.setVariable('ADVISORIES_HOST_ACCOUNT', 'ADVISORIES_HOST_ACCOUNT')
        binding.setVariable('env', [
                'METRICS_HOST_URL'     : 'sample.url',
                'ADVISORIES_HOST_URL'  : 'advisories.url',
                'AWS_ACCESS_KEY_ID'    : 'abc',
                'AWS_SECRET_ACCESS_KEY': 'xyz',
                'AWS_SESSION_TOKEN'    : 'sampleToken',
                'JOB_NAME'             : 'release-state',
                'BUILD_NUMBER'         : '7'
        ])
        super.setUp()
        // Schedule search returns one active release; writes return 201; other metrics searches return
        // no hits; gh (and everything else) returns empty so chores read them as "nothing found".
        helper.registerAllowedMethod('sh', [Map.class], { Map args ->
            String script = args.script
            if (script.contains('opensearch_release_schedule')) {
                return '{"hits":{"hits":[{"_source":{"version":"3.8.0","release_date":"2026-08-15","release_issue":"https://github.com/opensearch-project/opensearch-build/issues/6062","status":"active"}}]}}'
            }
            if (script.contains('-XPOST') || script.contains('-XPUT')) {
                return '201'
            }
            if (script.contains('_search')) {
                return '{"hits":{"hits":[]}}'
            }
            return ''
        })
    }

    @Test
    void testIndexesActiveReleaseWhenNoVersionGiven() {
        runScript('jenkins/release-workflows/release-state.jenkinsfile')
        assertThat(getCommandExecutions('echo', 'Indexing release state'),
                hasItem(containsString('Indexing release state for version 3.8.0.')))
    }

    @Test
    void testRestrictsToRequestedVersion() {
        addParam('VERSION', '3.8.0')
        runScript('jenkins/release-workflows/release-state.jenkinsfile')
        assertThat(getCommandExecutions('echo', 'Indexing release state'),
                hasItem(containsString('Indexing release state for version 3.8.0.')))
    }

    @Test
    void testSkipsWhenRequestedVersionIsNotActive() {
        addParam('VERSION', '9.9.9')
        runScript('jenkins/release-workflows/release-state.jenkinsfile')
        assertThat(getCommandExecutions('echo', 'No active releases'),
                hasItem(containsString('No active releases to index state for.')))
    }

    @Test
    void testRestrictsToRequestedCriteria() {
        addParam('CRITERIA', 'code_coverage_not_decreased')
        runScript('jenkins/release-workflows/release-state.jenkinsfile')
        assertThat(getCommandExecutions('echo', 'Restricting to criteria'),
                hasItem(containsString('Restricting to criteria: code_coverage_not_decreased.')))
    }

    @Test
    void testIndexesAllCriteriaWhenNoneRequested() {
        runScript('jenkins/release-workflows/release-state.jenkinsfile')
        assert getCommandExecutions('echo', 'Restricting to criteria').isEmpty()
    }

    @Test
    void testUpdateReleaseIssuesStageIsPresent() {
        runScript('jenkins/release-workflows/release-state.jenkinsfile')
        assertThat(getCommandExecutions('echo', 'Update Release Issues'),
                hasItem(containsString('Stage "Update Release Issues"')))
    }

    def getCommandExecutions(methodName, command) {
        def commands = helper.callStack.findAll {
            call ->
                call.methodName == methodName
        }.
        collect {
            call ->
                callArgsToString(call)
        }.findAll {
            output ->
                output.contains(command)
        }
        return commands
    }
}
