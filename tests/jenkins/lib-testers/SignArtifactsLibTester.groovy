import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class SignArtifactsLibTester extends LibFunctionTester {

    private String sigtype
    private String platform
    private String artifactPath
    private String type
    private String component

    public SignArtifactsLibTester(sigtype, platform, artifactPath, type, component){
        this.sigtype = sigtype
        this.platform = platform
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
        binding.setVariable('SIGN_ASM_ROLE', 'sign_asm_role')
        binding.setVariable('SIGN_ASM_ACCOUNT', 'sign_asm_account')
        binding.setVariable('SIGN_ASM_REGION', 'sign_asm_region')
        binding.setVariable('SIGN_ASM_KEYID', 'sign_asm_keyid')

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("withCredentials", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.artifactPath.first(), notNullValue())
        assertThat(call.args.platform.first(), notNullValue())
        if(call.args.artifactPath.first().toString().endsWith(".yml")){
            assertThat(call.args.type.first(), notNullValue())
        } else if(call.args.type.first() != 'maven'){
            assertThat(call.args.sigtype.first(), notNullValue())
        }
    }

    boolean expectedParametersMatcher(call) {
        if(call.args.artifactPath.first().toString().endsWith(".yml")){
            return call.args.platform.first().toString().equals(this.platform)
                    && call.args.artifactPath.first().toString().equals(this.artifactPath)
                    && call.args.type.first().toString().equals(this.type)
                    && (call.args.component.first() == null || call.args.component.first().toString().equals(this.component))
        } else {
            return call.args.sigtype.first().toString().equals(this.sigtype)
                    && call.args.platform.first().toString().equals(this.platform)
                    && call.args.artifactPath.first().toString().equals(this.artifactPath)
        }
    }

    String libFunctionName() {
        return 'signArtifacts'
    }
}
