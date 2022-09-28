/*
 * Copyright OpenSearch Contributors
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

class TestArchiveAssembleUpload extends BuildPipelineTest {
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('PUBLIC_ARTIFACT_URL', 'https://ci.opensearch.org/dbc')
        binding.setVariable('JOB_NAME', 'vars-build')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'artifact-bucket')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'account')
        binding.setVariable('STAGE_NAME', 'stage')
        binding.setVariable('BUILD_URL', 'http://jenkins.us-east-1.elb.amazonaws.com/job/vars/42')
        binding.setVariable('BUILD_NUMBER', '33')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'role')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', 'dummy')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'bucket')

        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("writeJSON", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod('unstash', [String.class], null)

        Path source = Path.of("tests/data/opensearch-build-1.3.0.yml");
        Path target = Path.of("tar/builds/opensearch/manifest.yml");
        Files.createDirectories(target.getParent());
        Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
    }

    @Test
    public void testSHAExists() {
        super.testPipeline("tests/jenkins/jobs/ArchiveAssembleUpload_Jenkinsfile")
    }
}
