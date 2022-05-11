import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDockerPromoteWithLatestTagEcrOnlyJob extends BuildPipelineTest {

    @Before
    void setUp() {
        String imageRepository = 'ci-runner-staging'
        String imageTag = '1.3.0'
        String accountName = 'aws_account_artifact'
        String sourceImagePath = "opensearchstaging/${imageRepository}:${imageTag}"

        this.registerLibTester(new CopyContainerLibTester(sourceImagePath,
                "public.ecr.aws/p5f6l6i3/${imageRepository}:${imageTag}",
                'ecr',
                'public.ecr.aws/p5f6l6i3',
                accountName))

        this.registerLibTester(new CopyContainerLibTester(sourceImagePath,
                "public.ecr.aws/p5f6l6i3/${imageRepository}:latest",
                'ecr',
                'public.ecr.aws/p5f6l6i3',
                accountName))

        super.setUp()

        binding.setVariable('IMAGE_REPOSITORY', imageRepository)
        binding.setVariable('IMAGE_TAG', imageTag)
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', accountName)
        binding.setVariable('DOCKER_HUB', false)
        binding.setVariable('ECR', true)
        binding.setVariable('TAG_LATEST', true)

    }

    @Test
    public void testDockerForEcrAndDockerhubJobProductionWithECR(){
        super.testPipeline("jenkins/docker-ecr/docker-ecr-promote.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-ecr-promote-with-latestTag-ECR-only.jenkinsfile")
    }

}
