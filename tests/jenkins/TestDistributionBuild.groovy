/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */
package test.jenkins
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

class TestDistributionBuild extends BuildPipelineTest {

    @Override   
    @Before
    void setUp() {

        super.setUp()

        def jobName = "dummy_job"
        def testManifest = "tests/jenkins/data/opensearch-dashboards-1.2.0-test.yml"
        def buildId = 215
        def buildManifest = "tests/jenkins/data/opensearch-dashboards-1.2.0-build.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch-dashboards/1.2.0/${buildId}/linux/x64/dist/opensearch-dashboards/opensearch-dashboards-1.2.0-linux-x64.tar.gz"
        def agentLabel = "Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host"

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.0.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
        )
        binding.setVariable('env', ['BUILD_NUMBER': '215'])
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_BUCKET_NAME')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'DUMMY_AWS_ACCOUNT_PUBLIC')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_ARTIFACT_BUCKET_NAME')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'DUMMY_PUBLIC_ARTIFACT_URL')
        binding.setVariable('env', ['BUILD_NUMBER': '215'])
        binding.setVariable('STAGE_NAME', 'DUMMY_STAGE_NAME')
        binding.setVariable('JOB_NAME', 'dummy_job')
        binding.setVariable('BUILD_NUMBER', '215')
        binding.setVariable('BUILD_URL', 'htth://BUILD_URL_dummy.com')
        binding.setVariable('WEBHOOK_URL', 'htth://WEBHOOK_URL_dummy.com')
        binding.setVariable('TEST_MANIFEST', testManifest)
        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('AGENT_LABEL', agentLabel)
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('BUILD_ID', "${buildId}")
        binding.setVariable('COMPONENT_NAME', 'OpenSearch-Dashboards')
        binding.setVariable('INPUT_MANIFEST', '2.0.0/opensearch-dashboards-2.0.0.yml')
        binding.setVariable('TEST_MANIFEST', '2.0.0/opensearch-dashboards-2.0.0-test.yml')
        binding.setVariable('INTEG_TEST_JOB_NAME', 'integ-test-opensearch-dashboards')
        binding.setVariable('BWC_TEST_JOB_NAME','bwc-test-opensearch-dashboards')
        binding.setVariable('BUILD_DOCKER','do_not_build_docker')
        binding.setVariable('PUBLISH_NOTIFICATION',true)
        binding.setVariable('AGENT_X64','Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host')
        binding.setVariable('AGENT_ARM64','Jenkins-Agent-AL2-Arm64-C6g4xlarge-Docker-Host')
        binding.setVariable('IMAGE_RPM','opensearchstaging/ci-runner:ci-runner-rockylinux8-opensearch-build-v2')
        // binding.setVariable('integ-test', ['getId':'123456'])
        // binding.setVariable('bwcTestResults', ['getId':'123456'])
        // binding.setVariable('getId', '123456')

        helper.registerAllowedMethod('beforeAgent', [Boolean.class], { args ->
            return true;
        })
        
        // def env = binding.getVariable('env')
        // env['dockerAgent'] = [image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11']
        binding.setVariable('env',[
            getId: '123456',
            dockerAgent: [image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11']
        ])

        helper.registerAllowedMethod("withCredentials", [Map])

        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((this.testManifest ?: binding.getVariable('TEST_MANIFEST') as File).text)
        })
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((buildManifest as File).text)
        })

        helper.registerAllowedMethod('writeYaml', [Map.class])

        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("s3Upload", [Map])

        helper.registerAllowedMethod('fileExists', [String.class], { args ->
            return true;
        })

        helper.registerAllowedMethod('findFiles', [Map.class], { f -> return fileList })

        // helper.registerAllowedMethod('integTestResults', [Map.class], {map ->
        //     return [['getId':'123456']]
        // })
        // helper.registerAllowedMethod('bwcTestResults', [Map.class], {map ->
        //     return [['getId':'123456']]
        // })
        // helper.registerAllowedMethod('skipIntegTests', [Boolean.class], { args ->
        //     return true;
        // })
        // helper.registerAllowedMethod('skipBwcTests', [Boolean.class], { args ->
        //     return true;
        // })
    }

    @Test
    public void testDistributionBuild_Pipeline() {
        // super.testPipeline("jenkins/opensearch-dashboards/distribution-build.jenkinsfile",
        // "tests/jenkins/jenkinsjob-regression-files/opensearch-dashboards/distribution-build.jenkinsfile")
        def script = loadScript("jenkins/opensearch-dashboards/distribution-build.jenkinsfile")

        // binding.setVariable('integ-test', ['getId':'123456'])
        // binding.setVariable('bwcTestResults', ['getId':'123456'])
        // helper.registerAllowedMethod('integ-test', [], {})
        // helper.registerAllowedMethod('skipIntegTests', [], {})
        // helper.registerAllowedMethod('buildInfoYaml', [], {})
        // helper.registerAllowedMethod('integTestResults', [], {})
        // helper.registerAllowedMethod('integ-test', [Map.class], {map ->
        //     return [['getId':'123456']]
        // })
        // helper.registerAllowedMethod('buildInfoYaml', [Map.class], {map ->
        //     return [['status':'123456']]
        // })
        // helper.registerAllowedMethod('skipIntegTests', [Boolean.class], { args ->
        //     return true;
        // })
        // helper.registerAllowedMethod('integ-test', [Map], { cmd ->
        //     return [getId: '123456'];
        // })
        script.run()
    }
}