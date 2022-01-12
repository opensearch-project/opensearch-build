/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import jenkins.tests.BaseJobPipelineTest
import org.junit.Before
import org.junit.Test

class TestDataPrepperDistributionArtifacts extends BaseJobPipelineTest {

    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('VERSION', '0.22.1')
        binding.setVariable('BRANCH', 'refs/tags/0.22.1')

        binding.setVariable('JOB_BASE_NAME', 'data-prepper-distribution-artifacts')
        binding.setVariable('BUILD_NUMBER', '7654321')
        binding.setVariable('WORKSPACE', '/tmp/workspace')

        binding.setVariable('ARTIFACT_BUCKET_NAME', 'job-s3-bucket-name')

        helper.registerAllowedMethod('checkout', [Map], {})
        helper.registerAllowedMethod('signArtifacts', [Map], {})
        helper.registerAllowedMethod('uploadToS3', [Map], {})
        helper.registerAllowedMethod('printArtifactDownloadUrlsForStaging', [Map], {})
        helper.registerAllowedMethod('postCleanup', [], {})
    }

    @Test
    void dataPrepperDistributionArtifacts_builds_consistently() {
        testPipeline('jenkins/data-prepper/distribution-artifacts.jenkinsfile',
                'tests/jenkins/jobs/data-prepper/distribution-artifacts.jenkinsfile')
    }
}
