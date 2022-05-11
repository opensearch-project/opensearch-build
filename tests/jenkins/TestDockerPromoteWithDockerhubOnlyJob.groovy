import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDockerPromoteWithDockerhubOnlyJob extends BuildPipelineTest {

    @Before
    void setUp() {
        String imageRepository = 'ci-runner-staging'
        String imageTag = 'latest'
        String accountName = 'aws_account_artifact'
        String sourceImagePath = "opensearchstaging/${imageRepository}:${imageTag}"

        this.registerLibTester(new CopyContainerLibTester(sourceImagePath,
                "opensearchproject/${imageRepository}:${imageTag}",
                'docker',
                'jenkins-staging-docker-prod-token'))

        super.setUp()

        binding.setVariable('IMAGE_REPOSITORY', imageRepository)
        binding.setVariable('IMAGE_TAG', imageTag)
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', accountName)
        binding.setVariable('DOCKER_HUB', true)
        binding.setVariable('ECR', false)
        binding.setVariable('TAG_LATEST', false)

    }

    @Test
    public void testDockerForEcrJobProductionWithDockerhubOnly(){
        super.testPipeline("jenkins/docker-ecr/docker-ecr-promote.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-ecr-promote-with-dockerhub-only.jenkinsfile")
    }

}
