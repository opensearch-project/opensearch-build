import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class CopyContainerLibTester extends LibFunctionTester {

    private final String sourceImage
    private final String destinationImage
    private final String destinationRegistry
    private final boolean prod

    CopyContainerLibTester(
        String sourceImage,
        String destinationImage,
        String destinationRegistry,
        boolean prod) {
        this.sourceImage = sourceImage
        this.destinationImage = destinationImage
        this.destinationRegistry = destinationRegistry
        this.prod = prod
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
        assertThat(call.args.sourceImage.first(), notNullValue())
        assertThat(call.args.destinationImage.first(), notNullValue())
        //assertThat(call.args.destinationType.first(),  notNullValue())
        assertThat(call.args.prod.first(), anyOf(equalTo(true),equalTo(false)))
    }

    boolean expectedParametersMatcher(call) {


        return call.args.sourceImage.first().toString().equals(sourceImage)
                && call.args.destinationImage.first().toString().equals(destinationImage)
                && call.args.destinationRegistry.first().equals(destinationRegistry)
    }

}

