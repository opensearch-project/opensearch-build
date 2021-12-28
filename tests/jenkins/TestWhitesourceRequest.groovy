/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*
import java.util.*

class TestWhitesourceRequest extends BuildPipelineTest {
    @Override
    @Before
    void setUp() {
        super.setUp()
        binding.setVariable('WORKSPACE', 'workspace')

        helper.registerAllowedMethod("readJSON", [Map]) { args ->
            return [:]
        }

        helper.registerAllowedMethod("httpRequest", [Map])
    }

    @Test
    public void test() {
        super.testPipeline("tests/jenkins/jobs/WhitesourceRequest_Jenkinsfile")
    }
}
