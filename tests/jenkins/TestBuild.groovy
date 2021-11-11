/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

import org.junit.*
import com.lesfurets.jenkins.unit.BasePipelineTest
import com.lesfurets.jenkins.unit.MethodCall
import static org.assertj.core.api.Assertions.assertThat

class TestBuild extends BasePipelineTest {
    def jenkinsScript = "tests/jenkins/jobs/build.groovy"

    @Override
    @Before
    void setUp() throws Exception {
        super.setUp()
    }

    // TODO: needs fix for https://github.com/jenkinsci/JenkinsPipelineUnit/issues/419
}
