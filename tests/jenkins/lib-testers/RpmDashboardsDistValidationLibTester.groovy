/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class RpmDashboardsDistValidationLibTester extends LibFunctionTester {

    private String bundleManifest
    private String rpmDistribution

    public RpmDashboardsDistValidationLibTester(rpmDistribution, bundleManifest){
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
        return 'rpmDashboardsDistValidation'
    }

    void configure(helper, binding){
    }

}
