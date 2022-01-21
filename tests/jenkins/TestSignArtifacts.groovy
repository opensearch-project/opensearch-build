/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


import jenkins.tests.BuildPipelineTest
import org.junit.*
import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class TestSignArtifacts extends BuildPipelineTest implements LibFunctionTester {

    public String signatureType
    public String distributionPlatform
    public String artifactPath

    @Before
    void setUp() {

        this.signatureType = '.sig'
        this.distributionPlatform = 'linux'
        this.artifactPath = "${this.workspace}/artifacts/"

        this.registerLibTester(new TestSignArtifacts(
                signatureType: signatureType,
                distributionPlatform: distributionPlatform,
                artifactPath: artifactPath
        ))

        super.setUp()

        binding.setVariable('DISTRIBUTION_PLATFORM', distributionPlatform)
        binding.setVariable('SIGNATURE_TYPE', signatureType)
        binding.setVariable('artifactPath', artifactPath)

    }

    @Test
    void testSignArtifacts() {
        super.testPipeline("tests/jenkins/jobs/SignArtifacts_Jenkinsfile")
    }

    void configure(helper, binding){
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        binding.setVariable('SIGNER_CLIENT_ROLE', 'dummy_signer_client_role')
        binding.setVariable('SIGNER_CLIENT_EXTERNAL_ID', 'signer_client_external_id')
        binding.setVariable('SIGNER_CLIENT_UNSIGNED_BUCKET', 'signer_client_unsigned_bucket')
        binding.setVariable('SIGNER_CLIENT_SIGNED_BUCKET', 'signer_client_signed_bucket')

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("withCredentials", [Map])
    }

    void verifyParams(helper) {
        assert helper.callStack.findAll { call ->
            call.methodName == 'signArtifacts'
        }.size() > 0

        helper.callStack.findAll { call ->
            call.methodName == 'signArtifacts'
        }.each { call ->
            assertThat(call.args.signatureType.first(), notNullValue())
            assertThat(call.args.signatureType.first(), anyOf(equalTo('.sig'), equalTo('.pgp')))
            assertThat(call.args.distributionPlatform.first(), notNullValue())
            assertThat(call.args.distributionPlatform.first(), anyOf(equalTo('linux')))
            assertThat(call.args.artifactPath.first(), notNullValue())
        }

        def callFound = false

        def callList = helper.callStack.findAll { call ->
            call.methodName == 'signArtifacts'
        }

        for(call in callList){
            if( call.args.signatureType.first() == this.signatureType
                    && call.args.distributionPlatform.first() == this.distributionPlatform
                    && call.args.artifactPath.first() == this.artifactPath){
                callFound = true
            }
        }

        assert callFound

    }
}
