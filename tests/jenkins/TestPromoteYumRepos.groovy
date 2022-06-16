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
import java.nio.file.*

class TestPromoteYumRepos extends BuildPipelineTest {

    @Override
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('PUBLIC_ARTIFACT_URL', 'https://ci.opensearch.org/dbc')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'artifactPromotionRole')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', 'artifactsAccount')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'prod-bucket-name')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        binding.setVariable('SIGNER_CLIENT_ROLE', 'dummy_signer_client_role')
        binding.setVariable('SIGNER_CLIENT_EXTERNAL_ID', 'signer_client_external_id')
        binding.setVariable('SIGNER_CLIENT_UNSIGNED_BUCKET', 'signer_client_unsigned_bucket')
        binding.setVariable('SIGNER_CLIENT_SIGNED_BUCKET', 'signer_client_signed_bucket')
        helper.registerAllowedMethod("git", [Map])
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
