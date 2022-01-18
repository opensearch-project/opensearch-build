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
    private Path targetOpenSearch;
    private Path targetOpenSearchDashboards;

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
        binding.setVariable('DISTRIBUTION_PLATFORM', 'linux')
        binding.setVariable('DISTRIBUTION_ARCHITECTURE', 'x64')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'downloadRoleName')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'publicAccount')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'artifactPromotionRole')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', 'artifactsAccount')
        binding.setVariable('ARTIFACT_PRODUCTION_BUCKET_NAME', 'prod-bucket-name')
        binding.setVariable('WORKSPACE', 'workspace')
        binding.setVariable('GITHUB_BOT_TOKEN_NAME', 'github_bot_token_name')
        binding.setVariable('SIGNER_CLIENT_ROLE', 'dummy_signer_client_role')
        binding.setVariable('SIGNER_CLIENT_EXTERNAL_ID', 'signer_client_external_id')
        binding.setVariable('SIGNER_CLIENT_UNSIGNED_BUCKET', 'signer_client_unsigned_bucket')
        binding.setVariable('SIGNER_CLIENT_SIGNED_BUCKET', 'signer_client_signed_bucket')

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
        helper.addFileExistsMock('workspace/artifacts/vars-build/1.3.0/33/linux/x64/builds/opensearch/core-plugins', true)

        helper.addShMock('find workspace/artifacts/vars-build/1.3.0/33/linux/x64/builds/opensearch/core-plugins -type f') { script ->
            return [stdout: "tar_dummy_artifact_1.0.0.tar.gz zip_dummy_artifact_1.1.0.zip dummy_artifact_1.1.0.dummy", exitValue: 0]
        }
        helper.addShMock('sha512sum tar_dummy_artifact_1.0.0.tar.gz') { script ->
            return [stdout: "shaHashDummy_tar_dummy_artifact_1.0.0.tar.gz  workspace/artifacts/vars-build/1.3.0/33/linux/x64/builds/opensearch/core-plugins/tar_dummy_artifact_1.0.0.tar.gz", exitValue: 0]
        }
        helper.addShMock('sha512sum zip_dummy_artifact_1.1.0.zip') { script ->
            return [stdout: "shaHashDummy_zip_dummy_artifact_1.1.0.zip  workspace/artifacts/vars-build/1.3.0/33/linux/x64/builds/opensearch/core-plugins/zip_dummy_artifact_1.1.0.zip", exitValue: 0]
        }
        helper.addShMock('basename workspace/artifacts/vars-build/1.3.0/33/linux/x64/builds/opensearch/core-plugins/tar_dummy_artifact_1.0.0.tar.gz') { script ->
            return [stdout: "tar_dummy_artifact_1.0.0.tar.gz", exitValue: 0]
        }
        helper.addShMock('basename workspace/artifacts/vars-build/1.3.0/33/linux/x64/builds/opensearch/core-plugins/zip_dummy_artifact_1.1.0.zip') { script ->
            return [stdout: "zip_dummy_artifact_1.1.0.zip", exitValue: 0]
        }

        targetOpenSearch = copy(
            "tests/data/opensearch-build-1.1.0.yml", 
            "artifacts/vars-build/1.3.0/33/linux/x64/builds/opensearch/manifest.yml"
        );

        targetOpenSearchDashboards = copy(
            "tests/data/opensearch-dashboards-build-1.2.0.yml", 
            "artifacts/vars-build/1.2.0/33/linux/x64/builds/opensearch-dashboards/manifest.yml"
        );
    }

    private Path copy(String sourcePath, String targetPath){
        Path source = Path.of(sourcePath);
        Path target = Path.of(targetPath);
        Files.createDirectories(target.getParent());
        Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);

        return target;
    }

    @After
    void after() {
        super.setUp()
        // Test file needs to be cleaned up
        Files.delete(targetOpenSearch)
        Files.delete(targetOpenSearchDashboards)
    }

    @Test
    public void testDefault() {
        super.testPipeline("tests/jenkins/jobs/PromoteArtifacts_Jenkinsfile")
    }

    @Test
    public void testDefault_OpenSearch_Dashboards() {
        super.testPipeline("tests/jenkins/jobs/PromoteArtifacts_OpenSearch_Dashboards_Jenkinsfile")
    }

    @Test
    public void testWithActions() {
        super.testPipeline("tests/jenkins/jobs/PromoteArtifacts_actions_Jenkinsfile")
    }

    @Test
    public void testWithActions_OpenSearch_Dashboards() {
        super.testPipeline("tests/jenkins/jobs/PromoteArtifacts_actions_OpenSearch_Dashboards_Jenkinsfile")
    }
}
