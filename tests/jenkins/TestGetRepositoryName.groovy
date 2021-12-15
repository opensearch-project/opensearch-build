/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests


import static org.assertj.core.api.Assertions.assertThat
import static org.assertj.core.api.Assertions.fail
import org.junit.*

class TestGetRepositoryName extends BuildPipelineTest {
    @Test
    void happyPath() {
        super.testPipeline("tests/jenkins/jobs/GetRepositoryName_happy_Jenkinsfile")
    }

    @Test
    void failurePath() {
        try {
            runScript("tests/jenkins/jobs/GetRepositoryName_failure_Jenkinsfile")
            fail("Exception should have been thrown")
        } catch (IllegalArgumentException iae) {
            assertThat(iae.message).isEqualTo("repository property was not set, try again with getRepositoryName('fooRepository')")
        }
    }
}
