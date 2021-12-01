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

class TestBuildAssembleUpload extends BuildPipelineTest {
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('BUILD_URL', 'http://jenkins.us-east-1.elb.amazonaws.com/job/vars/42')
        binding.setVariable('BUILD_NUMBER', '33')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'https://ci.opensearch.org/dbc')
        binding.setVariable('JOB_NAME', 'vars-build')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'artifact-bucket')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'account')
        binding.setVariable('STAGE_NAME', 'stage')

        helper.registerAllowedMethod("withCredentials", [List, Closure], { list, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod("sha1", [String], { filename ->
            return 'sha1'
        })

        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod("git", [Map])
    }

    @Test
    public void testIncremental() {
        helper.registerAllowedMethod("s3DoesObjectExist", [Map], { args ->
            return true
        })

        super.testPipeline(
            "tests/jenkins/jobs/BuildAssembleUpload_Jenkinsfile",
            "tests/jenkins/jobs/BuildAssembleUpload_Jenkinsfile_incremental"
        )
    }

    @Test
    public void testNotIncremental() {
        helper.registerAllowedMethod("s3DoesObjectExist", [Map], { args ->
            return false
        })

        super.testPipeline(
            "tests/jenkins/jobs/BuildAssembleUpload_Jenkinsfile",
            "tests/jenkins/jobs/BuildAssembleUpload_Jenkinsfile_not_incremental"
        )
    }
}
