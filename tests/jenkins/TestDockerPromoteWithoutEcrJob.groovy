import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDockerPromoteWithoutEcrJob extends BuildPipelineTest {

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
        binding.setVariable('RELEASE_TO_ECR', false)

    }

    @Test
    public void testDockerForEcrJobProductionWithoutECR(){
        super.testPipeline("jenkins/docker-ecr/docker-ecr-promote.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-ecr-promote-without-ECR.jenkinsfile")
    }

}
