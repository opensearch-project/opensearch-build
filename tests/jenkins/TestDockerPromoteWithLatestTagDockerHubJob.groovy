import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDockerPromoteWithLatestTagDockerHubJob extends BuildPipelineTest {

    @Before
    void setUp() {
        String imageRepository = 'ci-runner-staging'
        String imageTag = '1.3.0'
        String accountName = 'aws_account_artifact'
        String sourceImagePath = "opensearchstaging/${imageRepository}:${imageTag}"

        this.registerLibTester(new CopyContainerLibTester(sourceImagePath,
                "opensearchproject/${imageRepository}:${imageTag}",
                'docker',
                'jenkins-staging-docker-prod-token'))

        this.registerLibTester(new CopyContainerLibTester(sourceImagePath,
                "opensearchproject/${imageRepository}:latest",
                'docker',
                'jenkins-staging-docker-prod-token'))

        super.setUp()

        binding.setVariable('IMAGE_REPOSITORY', imageRepository)
        binding.setVariable('IMAGE_TAG', imageTag)
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', accountName)
        binding.setVariable('PLATFORM', 'docker-hub')
        binding.setVariable('TAG_LATEST', 'true')

    }

    @Test
    public void testDockerForEcrJobProductionWithDockerhubOnly(){
        super.testPipeline("jenkins/docker-ecr/docker-ecr-promote.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-ecr-promote-with-latestTag-dockerhub-only.jenkinsfile")
    }

}
