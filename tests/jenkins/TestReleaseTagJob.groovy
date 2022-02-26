/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */


import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestReleaseTagJob extends BuildPipelineTest {

    @Before
    void setUp() {

        def buildManifest = 'tests/data/opensearch-build-1.1.0.yml'

        def destPath = "tmp/workspace/${buildManifest}"

        def artifactsPath = 'distribution-build-opensearch/1.1.0/123/linux/x64/builds/opensearch/manifest.yml'

        def bucketName = 'job-s3-bucket-name'

        this.registerLibTester(new DownloadFromS3LibTester(destPath, bucketName, artifactsPath, true))

        this.registerLibTester(new CreateReleaseTagLibTester('tests/data/opensearch-build-1.1.0.yml', '1.1.0'))

        super.setUp()

        // Variables for Maven Sign Release job
        binding.setVariable('VERSION', '1.1.0')
        binding.setVariable('BUILD_ID', '123')
        binding.setVariable('ARTIFACT_BUCKET_NAME', bucketName)
        binding.setVariable('BUILD_MANIFEST', 'tests/data/opensearch-build-1.1.0.yml')
        binding.setVariable('WORKSPACE', 'tmp/workspace')

        helper.registerAllowedMethod('checkout', [Map], {})

    }

    @Test
    void ReleaseTag_test() {
        super.testPipeline('jenkins/release-tag/release-tag.jenkinsfile',
                'tests/jenkins/jenkinsjob-regression-files/release-tag/release-tag.jenkinsfile')
    }
}
