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


class TestPromoteArtifacts extends BuildPipelineTest {
    private Path target;

    @Override
    @Before
    void setUp() {
        super.setUp()

        binding.setVariable('PUBLIC_ARTIFACT_URL', 'https://ci.opensearch.org/dbc')
        binding.setVariable('DISTRIBUTION_JOB_NAME', 'vars-build')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'artifact-bucket')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'account')
        binding.setVariable('STAGE_NAME', 'stage')
        binding.setVariable('BUILD_URL', 'http://jenkins.us-east-1.elb.amazonaws.com/job/vars/42')
        binding.setVariable('DISTRIBUTION_BUILD_NUMBER', '33')
        binding.setVariable('DISTRIBUTION_PLATFORM', 'x64')
        binding.setVariable('DISTRIBUTION_ARCHITECTURE', 'linux')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'downloadRoleName')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'publicAccount')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'artifactPromotionRole')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', 'artifactsAccount')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'prod-bucket-name')
        binding.setVariable('WORKSPACE', 'workspace')
        
        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('getPath', { args ->
            return "workspace/file/found.zip"
        })
        helper.registerAllowedMethod('findFiles', [Map], { args ->
            return [{}]
        })

        Path source = Path.of("tests/data/opensearch-build-1.1.0.yml");
        target = Path.of("artifacts/vars-build/1.3.0/33/x64/linux/builds/opensearch/manifest.yml");
        Files.createDirectories(target.getParent());
        Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);    
    }

    @After
    void after() {
        super.setUp()
        Files.delete(target) // Test file needs to be cleaned up
    }

    @Test
    public void testDefault() {
        super.testPipeline("tests/jenkins/jobs/PromoteArtifacts_Jenkinsfile")
    }

    @Test
    public void testWithActions() {
        super.testPipeline("tests/jenkins/jobs/PromoteArtifacts_actions_Jenkinsfile")
    }
}
