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
                .defaultVersion('5.11.1')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )
        helper.registerAllowedMethod('parameterizedCron', [String], null)
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
        helper.addShMock("""date +%Y%m%d""") { script ->
            return [stdout: "20230619", exitValue: 0]
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
        assertThat(getCommandExecutions('parameterizedCron', ''), hasItem('\n            H 19 15 * * %PRODUCT=opensearch;TAG=1\n            H 19 15 * * %PRODUCT=opensearch-dashboards;TAG=1\n            H 19 15 * * %PRODUCT=opensearch;TAG=2\n            H 19 15 * * %PRODUCT=opensearch-dashboards;TAG=2\n        '))

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
