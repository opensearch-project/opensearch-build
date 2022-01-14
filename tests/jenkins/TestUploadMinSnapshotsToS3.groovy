/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import java.util.*

class TestUploadMinSnapshotsToS3 extends BuildPipelineTest {

    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('WORKSPACE', 'tests/data/')

        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'dummy_role')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', '1234')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'dummy_bucket')

        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    @Test
    public void test() {
        super.testPipeline("tests/jenkins/jobs/uploadSnapshotsToS3_Jenkinsfile")
    }  
}

