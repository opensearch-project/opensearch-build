import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDockerPromoteWithEcrOnlyJob extends BuildPipelineTest {

    @Before
    void setUp() {
        String imageRepository = 'ci-runner-staging'
        String imageTag = '2.0.0'
        String accountName = 'aws_account_artifact'
        Boolean latestTag = false
        Boolean majorVersionTag = true
        Boolean minorVersionTag = true

        this.registerLibTester(new CopyECRContainerLibTester(imageRepository,
                imageTag,
                latestTag,
                majorVersionTag,
                minorVersionTag))

        super.setUp()

        binding.setVariable('IMAGE_REPOSITORY', imageRepository)
        binding.setVariable('IMAGE_TAG', imageTag)
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', accountName)
        binding.setVariable('DOCKER_HUB', false)
        binding.setVariable('ECR', true)
        binding.setVariable('TAG_LATEST', false)
        binding.setVariable('TAG_MAJOR_VERSION', true)
        binding.setVariable('TAG_MAJOR_MINOR_VERSION', true)


    }

    @Test
    public void testDockerForEcrAndDockerhubJobProductionWithECR(){
        super.testPipeline("jenkins/docker-ecr/docker-ecr-promote.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-ecr-promote-with-ECR-only.jenkinsfile")
    }

}
