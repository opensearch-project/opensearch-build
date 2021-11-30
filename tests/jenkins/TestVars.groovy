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

class TestVars extends BuildPipelineTest {
    @Test
    public void testVars() {
        binding.setVariable('INPUT_MANIFEST', '1.2.0/opensearch-1.2.0.yml')
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

        binding.setVariable('WEBHOOK_URL', 'https://web/hook/url')

        helper.registerAllowedMethod("sha1", [String], { filename ->
            return 'sha1'
        })

        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("cleanWs", [Map])

        super.testPipeline("tests/jenkins/jobs/Vars_Jenkinsfile")
    }
}
