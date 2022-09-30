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

        this.registerLibTester(new DownloadFromS3LibTester(destPath, bucketName, artifactsPath, true))

        this.registerLibTester(new SignArtifactsLibTester( '.sig', 'linux',  manifestPath, 'maven', null))

        super.setUp()

        // Variables for Maven Sign Release job
        binding.setVariable('VERSION', '1.0.0')
        binding.setVariable('BUILD_ID', '123')
        binding.setVariable('ARTIFACT_PATH', 'distribution-build-opensearch/1.0.0/123/linux/x64/builds')
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)
        binding.setVariable('SONATYPE_STAGING_PROFILE_ID', 'dummy_id')

        helper.registerAllowedMethod('checkout', [Map], {})

        helper.registerSharedLibrary(
            library().name('jenkins')
                .defaultVersion('1.0.0')
                .allowOverride(true)
                .implicit(true)
                .targetPath('vars')
                .retriever(gitSource('https://github.com/opensearch-project/opensearch-build-libraries.git'))
                .build()
        )

    }

    @Test
    void MavenSignRelease_test() {
        super.testPipeline('jenkins/opensearch-maven-release/maven-sign-release.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/maven-sign-release/maven-sign-release.jenkinsfile')
    }
}
