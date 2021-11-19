/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import org.junit.*

class TestBuild extends BuildPipelineTest {
    @Test
    @Ignore // TODO: needs fix for https://github.com/jenkinsci/JenkinsPipelineUnit/issues/433 and https://github.com/jenkinsci/JenkinsPipelineUnit/issues/432
    void testBuild() {
        super.testPipeline("tests/jenkins/jobs/Build_Jenkinsfile")
    }
}
