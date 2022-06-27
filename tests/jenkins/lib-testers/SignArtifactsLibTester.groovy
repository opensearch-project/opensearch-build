import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class SignArtifactsLibTester extends LibFunctionTester {

    private String sigtype
    private String platform
    private String artifactPath
    private String type
    private String component

    public SignArtifactsLibTester(sigtype, platform, artifactPath, type, component) {
        this.sigtype = sigtype
        this.platform = platform
        this.artifactPath = artifactPath
        this.type = type
        this.component = component
    }

    void configure(helper, binding) {
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        if (this.sigtype.equals('.rpm')) {
            def configs = ['account': '1234',
            'passphrase_secrets_arn': 'ARN::123456',
            'secret_key_id_secrets_arn': 'ARN::56789',
            'key_id': 'abcd1234']
            binding.setVariable('configs', configs)
            helper.registerAllowedMethod('readJSON', [Map.class], { c -> configs })
        }
        else {
            def configs = ["role": "dummy_role",
                           "external_id": "dummy_ID",
                           "unsigned_bucket": "dummy_unsigned_bucket",
                           "signed_bucket": "dummy_signed_bucket"]
            binding.setVariable('configs', configs)
            helper.registerAllowedMethod('readJSON', [Map.class], { c -> configs })
        }
        helper.registerAllowedMethod('git', [Map])
        helper.registerAllowedMethod('withCredentials', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.artifactPath.first(), notNullValue())
        assertThat(call.args.platform.first(), notNullValue())
        if (call.args.artifactPath.first().toString().endsWith('.yml')) {
            assertThat(call.args.type.first(), notNullValue())
        } else if (call.args.type.first() != 'maven') {
            assertThat(call.args.sigtype.first(), notNullValue())
        }
    }

    boolean expectedParametersMatcher(call) {
        if (call.args.artifactPath.first().toString().endsWith('.yml')) {
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
