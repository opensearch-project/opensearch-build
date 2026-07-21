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

class TestReleaseSchedule extends BuildPipelineTest {

    static final String SAMPLE_HTML = '''
<table class="desktop-release-schedule-table">
<tr><th>Release Number</th><th>First RC Generated</th><th>Latest Possible Release Date</th><th>Release Manager</th><th>Tracking Issue</th></tr>
<tr><td>3.5.0</td><td>January 27th, 2026</td><td>February 10th, 2026</td><td><a href="https://github.com/foo">Foo</a></td><td><a href="https://github.com/opensearch-project/opensearch-build/issues/5897">5897</a></td></tr>
<tr><td>3.8.0</td><td><s>July 14th, 2026</s> July 21st, 2026</td><td>August 4th, 2026</td><td><a href="https://github.com/foo">Foo</a></td><td><a href="https://github.com/opensearch-project/opensearch-build/issues/6278">6278</a></td></tr>
</table>
'''

    @Override
    @Before
    void setUp() {
        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('add-release-indices')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/gaiksaya/opensearch-build-libraries.git'))
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
        binding.setVariable('METRICS_HOST_ACCOUNT', 'METRICS_HOST_ACCOUNT')
        binding.setVariable('env', [
                'METRICS_HOST_URL'     : 'sample.url',
                'AWS_ACCESS_KEY_ID'    : 'abc',
                'AWS_SECRET_ACCESS_KEY': 'xyz',
                'AWS_SESSION_TOKEN'    : 'sampleToken',
                'JOB_NAME'             : 'release-schedule-register',
                'BUILD_NUMBER'         : '7'
        ])
        super.setUp()
        // Single sh mock branching on the command: the page fetch returns the schedule HTML,
        // while cluster writes (curl to the metrics index) return 201 Created.
        helper.registerAllowedMethod('sh', [Map.class], { Map args ->
            return args.script.contains('releases.html') ? SAMPLE_HTML : '201'
        })
    }

    @Test
    void testRegistersEachParsedRelease() {
        addParam('RELEASES_URL', 'https://opensearch.org/releases.html')
        runScript('jenkins/release-workflows/release-schedule.jenkinsfile')
        assertThat(getCommandExecutions('echo', 'Parsed 2 release schedule row(s)'),
                hasItem(containsString('Parsed 2 release schedule row(s) from https://opensearch.org/releases.html.')))
        assertThat(getCommandExecutions('echo', 'Registering schedule for 3.5.0'),
                hasItem(containsString('Registering schedule for 3.5.0 (RC: 2026-01-27, Release: 2026-02-10).')))
        assertThat(getCommandExecutions('echo', 'Registering schedule for 3.8.0'),
                hasItem(containsString('Registering schedule for 3.8.0 (RC: 2026-07-21, Release: 2026-08-04).')))
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
