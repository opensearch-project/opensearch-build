/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test
import static com.lesfurets.jenkins.unit.global.lib.LibraryConfiguration.library
import static com.lesfurets.jenkins.unit.global.lib.GitSource.gitSource

class TestPromoteContainer extends BuildPipelineTest {

    String PROMOTE_PRODUCT = 'opensearch:2.0.1.2901, opensearch-dashboards:2.0.1-2345, data-prepper:2.0.1.123'
    String RELEASE_VERSION = '2.0.1'

    @Override
    @Before
    void setUp() {
        binding.setVariable('SOURCE_IMAGES', PROMOTE_PRODUCT)
        binding.setVariable('RELEASE_VERSION', RELEASE_VERSION)
        binding.setVariable('DOCKER_USERNAME', 'dummy_docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'dummy_docker_password')
        binding.setVariable('ARTIFACT_PROMOTION_ROLE_NAME', 'dummy-agent-AssumeRole')
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', '1234567890')
        binding.setVariable('DATA_PREPPER_STAGING_CONTAINER_REPOSITORY', 'dummy_dataprepper_ecr_url')


        helper.registerAllowedMethod('withAWS', [Map, Closure], null)
        super.setUp()

    }

    @Test
    public void testPromoteContainerToDocker() {
        String dockerPromote = true
        String ecrPromote = false
        String latestBoolean = false
        String majorVersionBoolean = false
        binding.setVariable('DOCKER_HUB_PROMOTE', dockerPromote)
        binding.setVariable('ECR_PROMOTE', ecrPromote)
        binding.setVariable('TAG_LATEST', latestBoolean)
        binding.setVariable('TAG_MAJOR_VERSION', majorVersionBoolean)

        super.testPipeline("jenkins/promotion/promote-docker-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/promotion/promote-container/promote-container-testPromoteContainerToDocker.jenkinsfile")
    }

    @Test
    public void testPromoteContainerToDockerLatest() {
        String dockerPromote = true
        String ecrPromote = false
        String latestBoolean = true
        String majorVersionBoolean = false
        binding.setVariable('DOCKER_HUB_PROMOTE', dockerPromote)
        binding.setVariable('ECR_PROMOTE', ecrPromote)
        binding.setVariable('TAG_LATEST', latestBoolean)
        binding.setVariable('TAG_MAJOR_VERSION', majorVersionBoolean)

        super.testPipeline("jenkins/promotion/promote-docker-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/promotion/promote-container/promote-container-testPromoteContainerToDockerLatest.jenkinsfile")
    }

    @Test
    public void testPromoteContainerToDockerMajor() {
        String dockerPromote = true
        String ecrPromote = false
        String latestBoolean = false
        String majorVersionBoolean = true
        binding.setVariable('DOCKER_HUB_PROMOTE', dockerPromote)
        binding.setVariable('ECR_PROMOTE', ecrPromote)
        binding.setVariable('TAG_LATEST', latestBoolean)
        binding.setVariable('TAG_MAJOR_VERSION', majorVersionBoolean)

        super.testPipeline("jenkins/promotion/promote-docker-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/promotion/promote-container/promote-container-testPromoteContainerToDockerMajor.jenkinsfile")
    }

    @Test
    public void testPromoteContainerToDockerLatestMajor() {
        String dockerPromote = true
        String ecrPromote = false
        String latestBoolean = true
        String majorVersionBoolean = true
        binding.setVariable('DOCKER_HUB_PROMOTE', dockerPromote)
        binding.setVariable('ECR_PROMOTE', ecrPromote)
        binding.setVariable('TAG_LATEST', latestBoolean)
        binding.setVariable('TAG_MAJOR_VERSION', majorVersionBoolean)

        super.testPipeline("jenkins/promotion/promote-docker-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/promotion/promote-container/promote-container-testPromoteContainerToDockerLatestMajor.jenkinsfile")
    }

    @Test
    public void testPromoteContainerToECRLatestMajor() {
        String dockerPromote = false
        String ecrPromote = true
        String latestBoolean = true
        String majorVersionBoolean = true
        binding.setVariable('DOCKER_HUB_PROMOTE', dockerPromote)
        binding.setVariable('ECR_PROMOTE', ecrPromote)
        binding.setVariable('TAG_LATEST', latestBoolean)
        binding.setVariable('TAG_MAJOR_VERSION', majorVersionBoolean)

        super.testPipeline("jenkins/promotion/promote-docker-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/promotion/promote-container/promote-container-testPromoteContainerToECRLatestMajor.jenkinsfile")
    }

    @Test
    public void testPromoteContainerToDockerECRLatestMajor() {
        String dockerPromote = true
        String ecrPromote = true
        String latestBoolean = true
        String majorVersionBoolean = true
        binding.setVariable('DOCKER_HUB_PROMOTE', dockerPromote)
        binding.setVariable('ECR_PROMOTE', ecrPromote)
        binding.setVariable('TAG_LATEST', latestBoolean)
        binding.setVariable('TAG_MAJOR_VERSION', majorVersionBoolean)

        super.testPipeline("jenkins/promotion/promote-docker-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/promotion/promote-container/promote-container-testPromoteContainerToDockerECRLatestMajor.jenkinsfile")
    }

}
