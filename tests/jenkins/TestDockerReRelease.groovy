/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.MatcherAssert.assertThat
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString


class TestDockerReRelease extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('5.6.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        super.setUp()

        // Variables
        addParam('PRODUCT', 'opensearch')
        addParam('TAG', '1')

        def inputManifest = "tests/jenkins/data/opensearch-1.3.0.yml"
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((inputManifest as File).text)
        })
        helper.addShMock("""docker inspect --format '{{ index .Config.Labels "org.label-schema.version"}}' opensearchproject/opensearch:1""") { script ->
            return [stdout: "1.3.0", exitValue: 0]
        }
        helper.addShMock("""docker inspect --format '{{ index .Config.Labels "org.label-schema.description"}}' opensearchproject/opensearch:1""") { script ->
            return [stdout: "7756", exitValue: 0]
        }
        helper.addShMock("""docker inspect --format '{{ index .Config.Labels "org.label-schema.build-date"}}' opensearchproject/opensearch:1""") { script ->
            return [stdout: "2023-06-19T19:12:59Z", exitValue: 0]
        }
        helper.addShMock("""docker inspect --format '{{ index .Config.Labels "org.label-schema.version"}}' opensearchproject/opensearch:latest""") { script ->
            return [stdout: "2.5.0", exitValue: 0]
        }

    }

    @Test
    void testReRelease() {
        super.testPipeline('jenkins/docker/docker-re-release.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/docker/docker-re-release.jenkinsfile')
    }

    @Test
    void checkForTriggeredJobs(){
        runScript('jenkins/docker/docker-re-release.jenkinsfile')
        assertThat(getCommandExecutions('build', ''), hasItem('{job=docker-build, propagate=true, wait=true, parameters=[null, null, null]}'))
        assertThat(getCommandExecutions('build', ''), hasItem('{job=docker-scan, propagate=true, wait=true, parameters=[null]}'))
        assertThat(getCommandExecutions('build', ''), hasItem('{job=docker-promotion, propagate=true, wait=true, parameters=[null, null, null]}'))

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
