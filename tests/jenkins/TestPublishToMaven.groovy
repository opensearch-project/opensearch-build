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

class TestPublishToMaven extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.5.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        super.setUp()
        binding.setVariable("BUILD_ID", "1234")
        binding.setVariable("VERSION", "2.1.0")
        binding.setVariable("ARTIFACT_BUCKET_NAME", "dummy-prod-bucket")
        binding.setVariable("BUILD_NUMBER", "234")
        binding.setVariable("GITHUB_BOT_TOKEN_NAME", "dummy_token")
        binding.setVariable("SONATYPE_STAGING_PROFILE_ID", "stag_abcd")
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("git", [Map])
    }

    @Test
    public void testMavenReleasePipeline() {
        super.testPipeline('jenkins/opensearch-maven-release/publish-to-maven.jenkinsfile', 'tests/jenkins/jenkinsjob-regression-files/opensearch-maven-release/publish-to-maven.jenkinsfile')
    }

    @Test
    public void verifyPublishing(){
        runScript("jenkins/opensearch-maven-release/publish-to-maven.jenkinsfile")
        def shellCommands = getCommandExecutions("sh" , "maven")
        assertThat(shellCommands, hasItem("/tmp/workspace/publish/stage-maven-release.sh /tmp/workspace/artifacts/distribution-build-opensearch/2.1.0/1234/linux/x64/tar/builds/opensearch/maven true"))
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
