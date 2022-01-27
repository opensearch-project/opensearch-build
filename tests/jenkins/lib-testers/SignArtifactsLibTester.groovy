import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class SignArtifactsLibTester extends LibFunctionTester {

    private String signatureType
    private String distributionPlatform
    private String artifactPath
    private String type
    private String component

    public SignArtifactsLibTester(signatureType, distributionPlatform, artifactPath, type, component){
        this.signatureType = signatureType
        this.distributionPlatform = distributionPlatform
        this.artifactPath = artifactPath
        this.type = type
        this.component = component
    }

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
        assertThat(call.args.artifactPath.first(), notNullValue())
        assertThat(call.args.distributionPlatform.first(), notNullValue())
        if(call.args.artifactPath.first().toString().endsWith(".yml")){
            assertThat(call.args.type.first(), notNullValue())
        } else {
            assertThat(call.args.signatureType.first(), notNullValue())
        }
    }

    boolean expectedParametersMatcher(call) {
        if(call.args.artifactPath.first().toString().endsWith(".yml")){
            return call.args.distributionPlatform.first().toString().equals(this.distributionPlatform)
                    && call.args.artifactPath.first().toString().equals(this.artifactPath)
                    && call.args.type.first().toString().equals(this.type)
                    && (call.args.component.first() == null || call.args.component.first().toString().equals(this.component))
        } else {
            return call.args.signatureType.first().toString().equals(this.signatureType)
                    && call.args.distributionPlatform.first().toString().equals(this.distributionPlatform)
                    && call.args.artifactPath.first().toString().equals(this.artifactPath)
        }
    }

    String libFunctionName() {
        return 'signArtifacts'
    }
}
