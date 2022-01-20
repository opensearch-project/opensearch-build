import jenkins.tests.BuildPipelineTest
import org.junit.Before
import org.junit.Test

class TestDockerPromoteJob extends BuildPipelineTest {

    def imageRepository = 'ci-runner-staging'
    def imageTag = 'latest'
    def sourceImagePath = "opensearchstaging/${imageRepository}:${imageTag}"

    @Before
    void setUp() {
        super.setUp()
        TestCopyDockerImage.setUpVariables(binding, helper)
    }

    @Test
    public void testDockerForEcrJobProduction(){

        def accountName = 'aws_account_artifact'

        binding.setVariable('IMAGE_REPOSITORY', imageRepository)
        binding.setVariable('IMAGE_TAG', imageTag)
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', accountName)

        helper.registerAllowedMethod("cleanWs", [Map])

        super.testPipeline("jenkins/docker-ecr/docker-promote.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-promote/docker-promote.jenkinsfile")

        TestCopyDockerImage.verifyCopyDockerImageParams(helper, sourceImagePath, "public.ecr.aws/p5f6l6i3/${imageRepository}:${imageTag}",
                'ecr', 'public.ecr.aws/p5f6l6i3', accountName)

        TestCopyDockerImage.verifyCopyDockerImageParams(helper, sourceImagePath, "opensearchproject/${imageRepository}:${imageTag}",
                'docker', 'jenkins-staging-docker-prod-token', accountName)
    }

}
