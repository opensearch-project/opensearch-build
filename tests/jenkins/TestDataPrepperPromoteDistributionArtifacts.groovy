/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestDataPrepperPromoteDistributionArtifacts extends BuildPipelineTest {

    private String version

    @Before
    void setUp() {
        super.setUp()

        version = '0.22.1'

        binding.setVariable('VERSION', version)
        binding.setVariable('SOURCE_JOB_BASE_NAME', 'data-prepper-distribution-artifacts')
        binding.setVariable('SOURCE_BUILD_NUMBER', '9876543')

        binding.setVariable('JOB_BASE_NAME', 'data-prepper-promote-distribution-artifacts')
        binding.setVariable('BUILD_NUMBER', '7654321')
        binding.setVariable('WORKSPACE', '/tmp/workspace')

        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'production-s3-bucket-name')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'production-role-name')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', 'aws-account-artifact')

        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod('s3Upload', [Map], {})
    }

    @Test
    void dataPrepperPromoteDistributionArtifacts_builds_consistently() {
        testPipeline('jenkins/data-prepper/promote-distribution-artifacts.jenkinsfile',
                'tests/jenkins/jobs/data-prepper/promote-distribution-artifacts.jenkinsfile')

        def actualS3Upload = helper.callStack.findAll { call ->
            call.methodName == 's3Upload'
        }.first()

        assertThat(actualS3Upload, notNullValue())
        assertThat(actualS3Upload.args[0].get('path'), equalTo("data-prepper/${version}/"))
    }
}
