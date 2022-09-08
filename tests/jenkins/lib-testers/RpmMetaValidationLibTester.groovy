/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class RpmMetaValidationLibTester extends LibFunctionTester {

    private String rpmDistribution
    private Map refMap

    public RpmMetaValidationLibTester(rpmDistribution, refMap){
        this.rpmDistribution = rpmDistribution
        this.refMap = refMap
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.rpmDistribution.first(), notNullValue())
        assertThat(call.args.refMap.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.rpmDistribution.first().toString().equals(this.rpmDistribution)
                && call.args.refMap.first().equals(this.refMap)
    }

    String libFunctionName(){
        return 'rpmMetaValidation'
    }

    void configure(helper, binding){
    }
}


