/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import com.lesfurets.jenkins.unit.*
import com.lesfurets.jenkins.unit.cps.BasePipelineTestCPS
import static groovy.test.GroovyAssert.*

class TestBuildFailureMessage extends BasePipelineTestCPS {

    def buildFailureMessage

    @Before
    @Override
    void setUp() {
        super.setUp()
        def currentBuild = binding.getVariable('currentBuild')
        binding.setVariable("currentBuild", currentBuild)
    }

    @Test
    void testCall() {
        buildFailureMessage = loadScript("../../vars/buildFailureMessage.groovy")
        printCallStack()
    }


}
