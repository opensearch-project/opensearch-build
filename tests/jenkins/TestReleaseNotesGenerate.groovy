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
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.assertj.core.api.Assertions.assertThat
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.CoreMatchers.hasItems

class TestReleaseNotesGenerate extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('11.0.1')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        super.setUp()

        binding.setVariable('INPUT_MANIFEST', 'tests/jenkins/data/opensearch-2.2.0.yml')
        binding.setVariable('GITHUB_USER', "GITHUB_USER")
        binding.setVariable('GITHUB_TOKEN', "GITHUB_TOKEN")
        binding.setVariable('MODEL_ID', 'test-model-id')
        binding.setVariable('MAX_TOKENS', '10000')
        binding.setVariable('BUILD_NUMBER', '12345')
        binding.setVariable('REF', 'main')
        binding.setVariable('GIT_LOG_DATE', '2025-06-24')
        binding.setVariable('WORKSPACE', '/tmp/workspace')
        helper.registerAllowedMethod("withSecrets", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("readYaml", [Map], {
            return new Yaml().load(('tests/jenkins/data/opensearch-2.2.0.yml' as File).text)
            //c -> lib.jenkins.InputManifest.new(readYaml(file: 'tests/jenkins/data/opensearch-2.2.0.yml'))
        })
        helper.registerAllowedMethod('unstash', [String.class], null)
        helper.registerAllowedMethod('stash', [String.class], null)
    }

    @Test
    public void releaseNotesCheckOpenSearchAndSql() {
        addParam('COMPONENTS', 'OpenSearch sql')
        super.testPipeline("jenkins/release-workflows/release-notes-generate.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/release-workflows/release-notes-generate.jenkinsfile")

        def callStack = helper.getCallStack()
        assertCallStack().contains('Release notes for OpenSearch=groovy.lang.Closure, Release notes for sql=groovy.lang.Closure')
        assertCallStack().contains('OpenSearch with index 0 will sleep 0 seconds to reduce load && sleep 0')
        assertCallStack().contains('sql with index 1 will sleep 30 seconds to reduce load && sleep 30')
        assertThat(helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.any { call ->
            callArgsToString(call).contains('./release_notes.sh generate manifests/tests/jenkins/data/opensearch-2.2.0.yml --component sql --date 2025-06-24 --max-tokens 10000 --ref main')
        }).isTrue()

        assertThat(helper.callStack.findAll { call ->
            call.methodName == 'sh'
        }.any { call ->
            callArgsToString(call).contains('./release_notes.sh generate manifests/tests/jenkins/data/opensearch-2.2.0.yml --component OpenSearch --date 2025-06-24 --max-tokens 10000 --ref main')
        }).isTrue()
    }
}
