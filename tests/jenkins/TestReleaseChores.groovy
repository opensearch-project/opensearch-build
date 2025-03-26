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
import static org.hamcrest.CoreMatchers.containsString
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static org.junit.jupiter.api.Assertions.assertThrows

class TestReleaseChores extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('8.4.1')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        helper.registerAllowedMethod("groovyScript", [Map])
        helper.registerAllowedMethod('activeChoice', [Map.class], null)
        helper.registerAllowedMethod('reactiveChoice', [Map.class], null)
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withCredentials", [Map])
        super.setUp()
    }

    @Test
    public void testVerifyParameters() {
        addParam('RELEASE_VERSION', '')
        addParam('RELEASE_CHORE', 'add_rc_details_comment')
        runScript('jenkins/release-workflows/release-chores.jenkinsfile')
        assertThat(getCommandExecutions('error', ''), hasItem('RELEASE_VERSION parameter cannot be empty!'))
    }

    @Test
    public void testParameterSetUp() {
        addParam('RELEASE_VERSION', '3.0.0-beta1')
        addParam('RELEASE_CHORE', 'checkReleaseOwners')
        addParam('ACTION', 'check')
        runScript('jenkins/release-workflows/release-chores.jenkinsfile')
        def callStack = helper.getCallStack()
        assertCallStack().contains('release-chores.groovyScript({fallbackScript={classpath=[], oldScript=, sandbox=true, script=return ["Unknown chore"]}, script={classpath=[], oldScript=, sandbox=true, script=return [ "checkReleaseOwners", "checkDocumentation", "checkCodeCoverage", "checkReleaseNotes", "checkReleaseIssues", "addRcDetailsComment" ]}})',
        'release-chores.activeChoice({name=RELEASE_CHORE, choiceType=PT_SINGLE_SELECT, description=Release chore to carry out, filterLength=1, filterable=false, randomName=choice-parameter-338807851658059, script=null})',
        'release-chores.groovyScript({fallbackScript={classpath=[], oldScript=, sandbox=true, script= return ["Unknown action"]}, script={classpath=[], oldScript=, sandbox=true, script=if (RELEASE_CHORE == "checkReleaseOwners") {\n' +
                '                    return ["check", "request", "assign" ]\n' +
                '                    } else if (RELEASE_CHORE == "checkDocumentation") {\n' +
                '                    return ["check", "notify"]\n' +
                '                    } else if (RELEASE_CHORE == "checkCodeCoverage") {\n' +
                '                    return ["check", "notify"]\n' +
                '                    } else if (RELEASE_CHORE == "checkReleaseNotes") {\n' +
                '                    return ["check", "notify"]\n' +
                '                    } else if (RELEASE_CHORE == "checkReleaseIssues") {\n' +
                '                    return ["check", "create"]\n' +
                '                    } else if (RELEASE_CHORE == "addRcDetailsComment") {\n' +
                '                    return ["add"]\n' +
                '                    }\n' +
                '                    else {\n' +
                '                    return ["Unknown chore"]\n' +
                '                    }}})',
        'release-chores.reactiveChoice({name=ACTION, choiceType=PT_SINGLE_SELECT, description=Release chore action, filterLength=1, filterable=false, randomName=choice-parameter-338807853238106, referencedParameters=RELEASE_CHORE, script=null})')
    }

    @Test
    public void testStageToLibMappingCheckReleaseOwners() {
        addParam('RELEASE_VERSION', '3.0.0-beta1')
        addParam('RELEASE_CHORE', 'checkReleaseOwners')
        addParam('ACTION', 'check')
        runScript('jenkins/release-workflows/release-chores.jenkinsfile')
        def callStack = helper.getCallStack()
        assertCallStack().contains('release-chores.stage(checkReleaseOwners, groovy.lang.Closure)')
        assertCallStack().contains('release-chores.checkRequestAssignReleaseOwners({inputManifest=[manifests/3.0.0-beta1/opensearch-3.0.0-beta1.yml, manifests/3.0.0-beta1/opensearch-dashboards-3.0.0-beta1.yml], action=check})')
    }

    @Test
    public void testStageToLibMappingCheckDocumentation() {
        addParam('RELEASE_VERSION', '3.0.0-beta1')
        addParam('RELEASE_CHORE', 'checkDocumentation')
        addParam('ACTION', 'check')
        runScript('jenkins/release-workflows/release-chores.jenkinsfile')
        def callStack = helper.getCallStack()
        assertCallStack().contains('release-chores.stage(checkDocumentationIssues, groovy.lang.Closure)')
        assertCallStack().contains('release-chores.checkDocumentationIssues({version=3.0.0-beta1, action=check})')
    }

    @Test
    public void testStageToLibMappingCheckCodeCoverage() {
        addParam('RELEASE_VERSION', '3.0.0-beta1')
        addParam('RELEASE_CHORE', 'checkCodeCoverage')
        addParam('ACTION', 'check')
        runScript('jenkins/release-workflows/release-chores.jenkinsfile')
        def callStack = helper.getCallStack()
        assertCallStack().contains('release-chores.stage(checkCodeCoverage, groovy.lang.Closure)')
        assertCallStack().contains('release-chores.checkCodeCoverage({inputManifest=[manifests/3.0.0-beta1/opensearch-3.0.0-beta1.yml, manifests/3.0.0-beta1/opensearch-dashboards-3.0.0-beta1.yml], action=check})')
    }

    @Test
    public void testStageToLibMappingCheckReleaseNotes() {
        addParam('RELEASE_VERSION', '3.0.0-beta1')
        addParam('RELEASE_CHORE', 'checkReleaseNotes')
        addParam('ACTION', 'check')
        addParam('GIT_LOG_DATE', '2025-03-19')
        assertThrows(Exception) {
            runScript('jenkins/release-workflows/release-chores.jenkinsfile')
        }
        def callStack = helper.getCallStack()
        assertThat(getCommandExecutions('sh', 'release_notes.sh'), hasItem(containsString('./release_notes.sh check manifests/3.0.0-beta1/opensearch-3.0.0-beta1.yml manifests/3.0.0-beta1/opensearch-dashboards-3.0.0-beta1.yml --date 2025-03-19 --output /tmp/workspace/table.md')))
        assertCallStack().contains('release-chores.stage(checkReleaseNotes, groovy.lang.Closure)')
        assertCallStack().contains('release-chores.checkReleaseNotes({version=3.0.0-beta1, dataTable=/tmp/workspace/table.md, action=check})')
    }

    @Test
    public void testStageToLibMappingCheckReleaseIssuess() {
        addParam('RELEASE_VERSION', '3.0.0-beta1')
        addParam('RELEASE_CHORE', 'checkReleaseIssues')
        addParam('ACTION', 'check')
            runScript('jenkins/release-workflows/release-chores.jenkinsfile')
        def callStack = helper.getCallStack()
        assertCallStack().contains('release-chores.stage(checkReleaseIssues, groovy.lang.Closure)')
        assertCallStack().contains('release-chores.checkReleaseIssues({version=3.0.0-beta1, inputManifest=[manifests/3.0.0-beta1/opensearch-3.0.0-beta1.yml, manifests/3.0.0-beta1/opensearch-dashboards-3.0.0-beta1.yml], action=check})')
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
