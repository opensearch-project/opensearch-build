/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins.tests

import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestUploadMinSnapshotsToS3 extends BuildPipelineTest {

    @Before
    void setUp() {
        List <Closure> fileActions = ['createSha512Checksums']
        this.registerLibTester(new UploadMinSnapshotsToS3LibTester( fileActions, 'tests/jenkins/data/opensearch-1.3.0.yml' ))
        super.setUp()
    }

    @Test
    public void test() {
        super.testPipeline("tests/jenkins/jobs/uploadMinSnapshotsToS3_Jenkinsfile")
    }  
}
