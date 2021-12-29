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

class TestBuildArchive extends BuildPipelineTest {
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('JOB_NAME', 'build-archive')
        binding.setVariable('STAGE_NAME', 'stage')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'account')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'artifact-bucket')

        helper.registerAllowedMethod("withCredentials", [List, Closure], { list, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod("zip", [Map])
        helper.registerAllowedMethod("git", [Map])
    }

    @Test
    public void testJenkinsfile() {
        super.testPipeline("tests/jenkins/jobs/BuildArchive_Jenkinsfile")
    }
}
