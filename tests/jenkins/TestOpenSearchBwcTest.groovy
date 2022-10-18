/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import org.yaml.snakeyaml.Yaml
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestOpenSearchBwcTest extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        super.setUp()

        def jobName = "dummy_job"
        def testManifest = "tests/jenkins/data/opensearch-1.3.0-test.yml"
        def buildId = 717
        def buildManifest = "tests/jenkins/data/opensearch-1.3.0-build.yml"
        def buildManifestUrl = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.0/${buildId}/linux/x64/dist/opensearch/opensearch-1.3.0-linux-x64.tar.gz"
        def agentLabel = "Jenkins-Agent-AL2-X64-C54xlarge-Docker-Host"

        binding.setVariable('env', ['BUILD_NUMBER': '717'])
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_BUCKET_NAME')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'DUMMY_AWS_ACCOUNT_PUBLIC')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_ARTIFACT_BUCKET_NAME')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'DUMMY_PUBLIC_ARTIFACT_URL')
        binding.setVariable('env', ['BUILD_NUMBER': '717'])
        binding.setVariable('STAGE_NAME', 'DUMMY_STAGE_NAME')
        binding.setVariable('JOB_NAME', 'dummy_job')
        binding.setVariable('BUILD_NUMBER', '717')
        binding.setVariable('BUILD_URL', 'htth://BUILD_URL_dummy.com')
        binding.setVariable('WEBHOOK_URL', 'htth://WEBHOOK_URL_dummy.com')
        binding.setVariable('TEST_MANIFEST', testManifest)
        binding.setVariable('BUILD_MANIFEST_URL', buildManifestUrl)
        binding.setVariable('AGENT_LABEL', agentLabel)
        binding.setVariable('BUILD_MANIFEST', buildManifest)
        binding.setVariable('BUILD_ID', "${buildId}")
        def env = binding.getVariable('env')
        env['DOCKER_AGENT'] = [image:'opensearchstaging/ci-runner:ci-runner-centos7-v1', args:'-e JAVA_HOME=/opt/java/openjdk-11']
        binding.getVariable('currentBuild').upstreamBuilds = [[fullProjectName: jobName]]

        helper.registerAllowedMethod("withCredentials", [Map])
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((this.testManifest ?: binding.getVariable('TEST_MANIFEST') as File).text)
        })
        helper.registerAllowedMethod('readYaml', [Map.class], { args ->
            return new Yaml().load((buildManifest as File).text)
        })
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("s3Upload", [Map]) 
        helper.registerAllowedMethod('fileExists', [String.class], { args ->
            return true;
        })
        helper.registerAllowedMethod('findFiles', [Map.class], null)
    }

    @Test
    void bwcTests_runs_consistently() {
        super.testPipeline('jenkins/opensearch/bwc-test.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch/bwc-test.jenkinsfile')
    }
}
