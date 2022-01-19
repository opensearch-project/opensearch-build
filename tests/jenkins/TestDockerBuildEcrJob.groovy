import jenkins.tests.BuildPipelineTest
import org.junit.*

class TestDockerBuildEcrJob extends BuildPipelineTest {

    def imageInStaging = 'ci-runner-staging:latest'
    def sourceImagePath = "opensearchstaging/${imageInStaging}"

    @Before
    void setUp() {
        super.setUp()
        TestCopyDockerImage.setUpVariables(binding, helper)
    }

    @Test
    public void testDockerForEcrJobStaging(){

        def accountName = 'aws_account_public'

        binding.setVariable('DOCKER_BUILD_SCRIPT_WITH_COMMANDS', 'dummy_command')
        binding.setVariable('DOCKER_USERNAME ', 'docker_username')
        binding.setVariable('DOCKER_PASSWORD', 'docker_password')
        binding.setVariable('IMAGE_IN_STAGING', imageInStaging)
        binding.setVariable('AWS_ACCOUNT_PUBLIC', accountName)

        binding.setVariable('ENVIRONMENT', 'staging')

        helper.registerAllowedMethod("git", [Map])
        helper.registerAllowedMethod("cleanWs", [Map])

        super.testPipeline("jenkins/docker-ecr/docker-build-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-build-ecr-staging.jenkinsfile")

        TestCopyDockerImage.verifyCopyDockerImageParams(helper, sourceImagePath, "public.ecr.aws/m0o1u6w1/${imageInStaging}",
                'ecr', 'public.ecr.aws/m0o1u6w1', accountName)

        }

    @Test
    public void testDockerForEcrJobProduction(){

        def imageInProd = 'ci-runner-prod:latest'
        def accountName = 'aws_account_artifact'

        binding.setVariable('IMAGE_IN_STAGING', imageInStaging)
        binding.setVariable('IMAGE_IN_PROD', imageInProd)
        binding.setVariable('AWS_ACCOUNT_ARTIFACT', accountName)
        binding.setVariable('ENVIRONMENT', 'production')

        helper.registerAllowedMethod("cleanWs", [Map])

        super.testPipeline("jenkins/docker-ecr/docker-build-ecr.jenkinsfile",
                "tests/jenkins/jenkinsjob-regression-files/docker-ecr/docker-build-ecr-production.jenkinsfile")

        TestCopyDockerImage.verifyCopyDockerImageParams(helper, sourceImagePath, "public.ecr.aws/p5f6l6i3/${imageInProd}",
                'ecr', 'public.ecr.aws/p5f6l6i3', accountName)

        TestCopyDockerImage.verifyCopyDockerImageParams(helper, sourceImagePath, "opensearchproject/${imageInProd}",
                'docker', 'jenkins-staging-docker-prod-token', accountName)
    }

}
