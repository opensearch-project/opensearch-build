/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

class BuildFailureMessageLibTester extends LibFunctionTester {


    public BuildFailureMessageLibTester() {}


     void parameterInvariantsAssertions(call) {
          //N/A
     }

     boolean expectedParametersMatcher(call) {
        return true
     }


    String libFunctionName() {
        return 'buildFailureMessage'
    }

    void configure(helper, binding){
    }
}
