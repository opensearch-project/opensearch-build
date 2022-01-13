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
import java.nio.file.*

class UploadMinSnapshotsToS3 extends BuildPipelineTest {
    private Path target;

    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('WORKSPACE', 'workspace')

        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'dummy_role')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', '1234')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'dummy_bucket')

        Path source = Path.of("tests/data/opensearch-build-1.1.0.yml");
        target = Path.of("workspace/builds/opensearch/manifest.yml");
        Files.createDirectories(target.getParent());
        Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);

        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }
    @Test
    public void test() {
        super.testPipeline("tests/jenkins/jobs/uploadSnapshotsToS3_Jenkinsfile")
    }
    
    @After
    void after() {
        super.setUp()
        Files.delete(target) // Test file needs to be cleaned up
    }
}

