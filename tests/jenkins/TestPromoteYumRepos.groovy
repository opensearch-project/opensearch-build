/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import java.util.*
import java.nio.file.*

class TestPromoteYumRepos extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('PUBLIC_ARTIFACT_URL', 'https://ci.opensearch.org/dbc')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        def configs = ["role": "dummy_role",
                       "external_id": "dummy_ID",
                       "unsigned_bucket": "dummy_unsigned_bucket",
                       "signed_bucket": "dummy_signed_bucket"]
        binding.setVariable('configs', configs)
        helper.registerAllowedMethod("readJSON", [Map.class], {c -> configs})
        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

    }

    @Test
    public void testDefault() {
        super.testPipeline("tests/jenkins/jobs/PromoteYumRepos_Jenkinsfile")
    }
}
