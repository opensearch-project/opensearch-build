/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestMavenSignReleaseJob extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {

        def destPath = "${this.workspace}/artifacts"

        def manifestPath = "${this.workspace}/artifacts/distribution-build-opensearch/1.0.0/123/linux/x64/builds/opensearch/manifest.yml"

        def artifactsPath = 'distribution-build-opensearch/1.0.0/123/linux/x64/builds/'

        def bucketName = 'job-s3-bucket-name'

        // this.registerLibTester(new DownloadFromS3LibTester(destPath, bucketName, artifactsPath, true))
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        // this.registerLibTester(new SignArtifactsLibTester( '.sig', 'linux',  manifestPath, 'maven', null))
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        helper.registerAllowedMethod('git', [Map])
        helper.registerAllowedMethod('withCredentials', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        super.setUp()

        // Variables for Maven Sign Release job
        binding.setVariable('VERSION', '1.0.0')
        binding.setVariable('BUILD_ID', '123')
        binding.setVariable('ARTIFACT_PATH', 'distribution-build-opensearch/1.0.0/123/linux/x64/builds')
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)
        binding.setVariable('SONATYPE_STAGING_PROFILE_ID', 'dummy_id')

        helper.registerAllowedMethod('checkout', [Map], {})

    }

    @Test
    void MavenSignRelease_test() {
        super.testPipeline('jenkins/opensearch-maven-release/maven-sign-release.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/maven-sign-release/maven-sign-release.jenkinsfile')
    }
}
