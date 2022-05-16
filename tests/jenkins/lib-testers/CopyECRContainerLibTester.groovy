import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class CopyECRContainerLibTester extends LibFunctionTester {

    private final String imageRepository
    private final String imageTag
    private final Boolean latestTag
    private final Boolean majorVersionTag
    private final Boolean minorVersionTag

    CopyECRContainerLibTester(
            String imageRepository,
            String imageTag,
            Boolean latestTag,
            Boolean majorVersionTag,
            Boolean minorVersionTag) {
        this.imageRepository = imageRepository
        this.imageTag = imageTag
        this.latestTag = latestTag
        this.majorVersionTag = majorVersionTag
        this.minorVersionTag = minorVersionTag
    }

    String libFunctionName() {
        return 'copyECRContainer'
    }

    void configure(helper, binding){
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', 'DUMMY_ACCOUNT_NAME')
        helper.registerAllowedMethod('withAWS', [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.imageRepository.first(), notNullValue())
        assertThat(call.args.imageTag.first(), notNullValue())
        assertThat(call.args.latestTag.first().toString(), anyOf(equalTo('true'), equalTo('false')))
        assertThat(call.args.majorVersionTag.first().toString(), anyOf(equalTo('true'), equalTo('false')))
        assertThat(call.args.minorVersionTag.first().toString(), anyOf(equalTo('true'), equalTo('false')))
    }

    boolean expectedParametersMatcher(call) {
        return call.args.imageRepository.first().toString().equals(imageRepository)
                && call.args.imageTag.first().toString().equals(imageTag)
                && call.args.latestTag.first().toString().equals(latestTag.toString())
                && call.args.majorVersionTag.first().toString().equals(majorVersionTag.toString())
                && call.args.minorVersionTag.first().toString().equals(minorVersionTag.toString())
    }

}
