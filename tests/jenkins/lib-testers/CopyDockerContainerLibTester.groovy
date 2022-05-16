import jnr.ffi.Struct

import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class CopyDockerContainerLibTester extends LibFunctionTester {

    private final String imageRepository
    private final String imageTag
    private final Boolean latestTag
    private final Boolean majorVersionTag
    private final Boolean minorVersionTag

    CopyDockerContainerLibTester(
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
        return 'copyDockerContainer'
    }

    void configure(helper, binding){
        binding.setVariable('DOCKER_USERNAME', 'dummy_docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'dummy_docker_password')
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
