/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.MethodCall.callArgsToString
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.hasItem
import static org.hamcrest.CoreMatchers.hasItems
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource
import org.yaml.snakeyaml.Yaml

class TestPublishMinSnapshots extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('5.12.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
            )

        super.setUp()
        // Variables
        // addParam('INPUT_MANIFEST','3.0.0/opensearch-3.0.0.yml') - to be added after upgrading unit testing library
        binding.setVariable('INPUT_MANIFEST', '3.0.0/opensearch-3.0.0.yml')
        binding.setVariable('AGENT_LINUX_X64', 'Jenkins-Agent-AL2023-X64-C54xlarge-Docker-Host')
        binding.setVariable('AGENT_LINUX_ARM64', 'Jenkins-Agent-AL2023-Arm64-C6g4xlarge-Docker-Host')
        binding.setVariable('AGENT_MACOS_X64', 'Jenkins-Agent-MacOS12-X64-Mac1Metal-Multi-Host')
        binding.setVariable('AGENT_WINDOWS_X64', 'Jenkins-Agent-Windows2019-X64-C54xlarge-Docker-Host')
        binding.setVariable('IMAGE_WINDOWS_ZIP', 'opensearchstaging/ci-runner:ci-runner-windows2019-servercore-opensearch-build-v1')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'production-s3-bucket-name')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'production-role-name')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', 'aws-account-artifact')
        binding.setVariable('dockerAgent', [image:'opensearchstaging/ci-runner:ci-runner-centos7-opensearch-build-v3', args:'-e JAVA_HOME=/opt/java/openjdk-20'])
        helper.registerAllowedMethod('withCredentials', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('s3Upload', [Map], {})
    }

    @Test
    void TestPublishMinSnapshotsUploads(){
        String currentStage = null
        helper.registerAllowedMethod('stage', [String, Closure]) { name, body ->
            currentStage = name
            body()
        }
        helper.registerAllowedMethod('readYaml', [Map]) { args ->
            switch (currentStage) {
                case 'linux-x64-tar':
                    return new Yaml().load(('tests/jenkins/data/opensearch-min-3.0.0-snapshot-linux-x64-build-manifest.yml' as File).text)
                case 'linux-arm64-tar':
                    return new Yaml().load(('tests/jenkins/data/opensearch-min-3.0.0-snapshot-linux-arm64-build-manifest.yml' as File).text)
                case 'macos-x64-tar':
                    return new Yaml().load(('tests/jenkins/data/opensearch-min-3.0.0-snapshot-darwin-build-manifest.yml' as File).text)
                case 'windows-x64-zip':
                    return new Yaml().load(('tests/jenkins/data/opensearch-min-3.0.0-snapshot-windows-build-manifest.yml' as File).text)
                default:
                    return new Yaml().load(('tests/jenkins/data/opensearch-min-3.0.0-snapshot-linux-x64-build-manifest.yml' as File).text)
            }
        }
        super.testPipeline('jenkins/opensearch/publish-min-snapshots.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/opensearch/publish-min-snapshots.jenkinsfile')
        assertThat(getCommands('sh', 'tar'), hasItem('./build.sh manifests/3.0.0/opensearch-3.0.0.yml -d tar --component OpenSearch -p linux -a x64 --snapshot'))
        assertThat(getCommands('sh', 'tar'), hasItem('./build.sh manifests/3.0.0/opensearch-3.0.0.yml -d tar --component OpenSearch -p linux -a arm64 --snapshot'))
        assertThat(getCommands('sh', 'windows'), hasItem('./build.sh manifests/3.0.0/opensearch-3.0.0.yml -d zip --component OpenSearch -p windows -a x64 --snapshot'))
        assertThat(getCommands('sh', 'darwin'), hasItem('./build.sh manifests/3.0.0/opensearch-3.0.0.yml -d tar --component OpenSearch -p darwin -a x64 --snapshot'))
        assertThat(getCommands('s3Upload', 'min-3.0.0-SNAPSHOT'), hasItems(
            //linux-x64-tar
            '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-linux-x64-latest.tar.gz, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-linux-x64-latest.tar.gz}',
            '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-linux-x64-latest.tar.gz.sha512, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-linux-x64-latest.tar.gz.sha512}',
            '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-linux-x64-latest.tar.gz.build-manifest.yml, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-linux-x64-latest.tar.gz.build-manifest.yml}',
            //linux-arm64-tar
            '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-linux-arm64-latest.tar.gz, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-linux-arm64-latest.tar.gz}',
            '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-linux-arm64-latest.tar.gz.sha512, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-linux-arm64-latest.tar.gz.sha512}',
            '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-linux-arm64-latest.tar.gz.build-manifest.yml, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-linux-arm64-latest.tar.gz.build-manifest.yml}',
            // window-x64-upload
            '{file=/tmp/workspace/zip/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-windows-x64-latest.zip, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-windows-x64-latest.zip}',
            '{file=/tmp/workspace/zip/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-windows-x64-latest.zip.sha512, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-windows-x64-latest.zip.sha512}',
            '{file=/tmp/workspace/zip/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-windows-x64-latest.zip.build-manifest.yml, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-windows-x64-latest.zip.build-manifest.yml}',
            // macos-x64-upload
            '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-darwin-x64-latest.tar.gz, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-darwin-x64-latest.tar.gz}',
            '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-darwin-x64-latest.tar.gz.sha512, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-darwin-x64-latest.tar.gz.sha512}', '{file=/tmp/workspace/tar/builds/opensearch/dist/opensearch-min-3.0.0-SNAPSHOT-darwin-x64-latest.tar.gz.build-manifest.yml, bucket=ARTIFACT_PRODUCTION_BUCKET_NAME, path=snapshots/core/opensearch/3.0.0-SNAPSHOT/opensearch-min-3.0.0-SNAPSHOT-darwin-x64-latest.tar.gz.build-manifest.yml}'))
    }

    def getCommands(String methodName, String commandString) {
        def shCurlCommands = helper.callStack.findAll { call ->
            call.methodName == methodName
        }.collect { call ->
            callArgsToString(call)
        }.findAll { externalCommand ->
            externalCommand.contains(commandString)
        }
        return shCurlCommands
    }
}
