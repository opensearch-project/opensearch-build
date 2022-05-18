import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class CopyContainerLibTester extends LibFunctionTester {

    private final String sourceImagePath
    private final String destinationImagePath
    private final String destinationType

    CopyContainerLibTester(
        String sourceImagePath,
        String destinationImagePath,
        String destinationType,
        boolean ecrProd=false) {
        this.sourceImagePath = sourceImagePath
        this.destinationImagePath = destinationImagePath
        this.destinationType = destinationType
        this.destinationCredentialIdentifier = destinationCredentialIdentifier
        this.ecrProd = ecrProd
    }

    String libFunctionName() {
        return 'copyContainer'
    }

    void configure(helper, binding){
        binding.setVariable('DOCKER_USERNAME', 'dummy_docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'dummy_docker_password')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'sample-agent-AssumeRole')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', '1234567890')

        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.sourceImagePath.first(), notNullValue())
        assertThat(call.args.destinationImagePath.first(), notNullValue())
        assertThat(call.args.destinationType.first(), notNullValue())
        assertThat(call.args.destinationType.first(), anyOf(equalTo('Prod-ECR'), equalTo('Prod-DockerHub'), equalTo('Staging-ECR'), equalTo('Staging-DockerHub')))
    }

    boolean expectedParametersMatcher(call) {

        return call.args.sourceImagePath.first().toString().equals(sourceImagePath)
                && call.args.destinationImagePath.first().toString().equals(destinationImagePath)
                && call.args.destinationType.first().toString().equals(destinationType)
    }

}
