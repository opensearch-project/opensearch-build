/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.*
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestSignArtifacts extends BuildPipelineTest {

    private String signatureType
    private String distributionPlatform
    private String artifactPath

    public LibTester libTester = new LibTester()

    @Before
    void setUp() {

        this.registerLibTester(new TestSignArtifacts(
                signatureType: '.sig',
                distributionPlatform: 'linux',
                artifactPath: "${this.workspace}/artifacts/"
        ).libTester)

        super.setUp()
    }

    @Test
    void testSignArtifacts() {
        super.testPipeline("tests/jenkins/jobs/SignArtifacts_Jenkinsfile")
    }

    class LibTester extends LibFunctionTester {

        void configure(helper, binding) {
            binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
            binding.setVariable('SIGNER_CLIENT_ROLE', 'dummy_signer_client_role')
            binding.setVariable('SIGNER_CLIENT_EXTERNAL_ID', 'signer_client_external_id')
            binding.setVariable('SIGNER_CLIENT_UNSIGNED_BUCKET', 'signer_client_unsigned_bucket')
            binding.setVariable('SIGNER_CLIENT_SIGNED_BUCKET', 'signer_client_signed_bucket')

            helper.registerAllowedMethod("git", [Map])
            helper.registerAllowedMethod("withCredentials", [Map])
        }

        void parameterInvariantsAssertions(call) {
            assertThat(call.args.signatureType.first(), notNullValue())
            assertThat(call.args.distributionPlatform.first(), notNullValue())
            assertThat(call.args.artifactPath.first(), notNullValue())
        }

        boolean expectedParametersMatcher(call) {
            return call.args.signatureType.first() == this.signatureType
                    && call.args.distributionPlatform.first() == this.distributionPlatform
                    && call.args.artifactPath.first() == this.artifactPath
        }

        String libFunctionName() {
            return 'signArtifacts'
        }
    }
}
