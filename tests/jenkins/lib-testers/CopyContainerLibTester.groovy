import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class CopyContainerLibTester extends LibFunctionTester {

    private final String sourceImagePath
    private final String destinationImagePath
    private final String destinationType
    private final String destinationCredentialIdentifier
    private final String accountName

    CopyContainerLibTester(
        String sourceImagePath,
        String destinationImagePath,
        String destinationType,
        String destinationCredentialIdentifier,
        String accountName=null) {
        this.sourceImagePath = sourceImagePath
        this.destinationImagePath = destinationImagePath
        this.destinationType = destinationType
        this.destinationCredentialIdentifier = destinationCredentialIdentifier
        this.accountName = accountName
    }

    String libFunctionName() {
        return 'copyContainer'
    }

    void configure(helper, binding){
        binding.setVariable('DOCKER_USERNAME', 'dummy_docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'dummy_docker_password')

        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.sourceImagePath.first(), notNullValue())
        assertThat(call.args.destinationImagePath.first(), notNullValue())
        assertThat(call.args.destinationType.first(), notNullValue())
        assertThat(call.args.destinationType.first(), anyOf(equalTo('ecr'), equalTo('docker')))
        assertThat(call.args.destinationCredentialIdentifier.first(), notNullValue())
        if (call.args.destinationType.first().toString() == 'docker') {
            assertThat(
                call.args.destinationCredentialIdentifier.first(),
                anyOf(
                    equalTo('jenkins-staging-docker-prod-token'),
                    equalTo('jenkins-staging-docker-staging-credential')))
        }
        if (call.args.destinationType.first().toString() == 'ecr') {
            assertThat(call.args.accountName.first(), notNullValue())
            assertThat(call.args.destinationCredentialIdentifier.first(),
                anyOf(
                    equalTo('public.ecr.aws/p5f6l6i3'),
                    equalTo('public.ecr.aws/m0o1u6w1')))
        }
    }

    boolean expectedParametersMatcher(call) {
        boolean accountNameFound = true

        if (call.args.destinationType.first() == 'ecr') {
            accountNameFound = call.args.accountName.first().toString() == accountName
        }

        return call.args.sourceImagePath.first().toString().equals(sourceImagePath)
                && call.args.destinationImagePath.first().toString().equals(destinationImagePath)
                && call.args.destinationCredentialIdentifier.first().toString().equals(destinationCredentialIdentifier)
                && call.args.destinationType.first().toString().equals(destinationType)
                && accountNameFound
    }

}
