
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class RpmOpenSearchDistValidationLibTester extends LibFunctionTester {

    private String bundleManifest
    private String rpmDistribution

    public RpmOpenSearchDistValidationLibTester(rpmDistribution, bundleManifest){
        this.rpmDistribution = rpmDistribution
        this.bundleManifest = bundleManifest
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.rpmDistribution.first(), notNullValue())
        assertThat(call.args.bundleManifest.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.rpmDistribution.first().toString().equals(this.rpmDistribution)
                && call.args.bundleManifest.first().equals(this.bundleManifest)
    }

    String libFunctionName(){
        return 'rpmOpenSearchDistValidation'
    }

    void configure(helper, binding){
    }

}



