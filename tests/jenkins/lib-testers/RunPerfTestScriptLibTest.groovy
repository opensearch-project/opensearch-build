import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class RunPerfTestScriptLibTester extends LibFunctionTester {

    private String bundleManifest
    private String buildId
    private String insecure
    private String workload
    private String testIterations
    private String warmupIterations
    private boolean security

    public RunPerfTestScriptLibTester(bundleManifest, buildId, insecure, workload,
        testIterations, warmupIterations, security) {
        this.bundleManifest = bundleManifest
        this.buildId = buildId
        this.insecure = insecure
        this.workload = workload
        this.testIterations = testIterations
        this.warmupIterations = warmupIterations
        this.security = security
    }

    void configure(helper, binding) {
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("uploadTestResults", [Map])
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], {
            args,
            closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod('findFiles', [Map.class], null)
        helper.registerAllowedMethod("withCredentials", [Map])
        helper.registerAllowedMethod("downloadBuildManifest", [Map], {
            c -> lib.jenkins.BuildManifest.new(readYaml(file: bundleManifest))
        })

        binding.setVariable('AGENT_LABEL', 'Jenkins-Agent-al2-x64-c54xlarge-Docker-Host')
        binding.setVariable('AGENT_IMAGE', 'opensearchstaging/ci-runner:ci-runner-centos7-v1')
        binding.setVariable('ARCHITECTURE', 'x64')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'test_bucket')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('BUILD_ID', buildId)
        binding.setVariable('BUILD_NUMBER', buildId)
        binding.setVariable('BUILD_URL', 'test://artifact.url')
        binding.setVariable('BUNDLE_MANIFEST', bundleManifest)
        binding.setVariable('BUNDLE_MANIFEST_URL', 'test://artifact.url')
        binding.setVariable('GITHUB_TOKEN', 'test_token')
        binding.setVariable('HAS_SECURITY', security)
        binding.setVariable('JOB_NAME', 'perf-test')
        binding.setVariable('PERF_TEST_CONFIG_LOCATION', 'test_config')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'test://artifact.url')
        binding.setVariable('STAGE_NAME', 'test_stage')
        binding.setVariable('TEST_ITERATIONS', testIterations)
        binding.setVariable('TEST_WORKLOAD', workload)
        binding.setVariable('WEBHOOK_URL', 'test://artifact.url')
        binding.setVariable('WARMUP_ITERATIONS', warmupIterations)

    }

    void parameterInvariantsAssertions(call) {
        assertThat(call.args.bundleManifest.first(), notNullValue())
        assertThat(call.args.buildId.first(), notNullValue())
        assertThat(call.args.insecure.first(), notNullValue())
        assertThat(call.args.workload.first(), notNullValue())
        assertThat(call.args.testIterations.first(), notNullValue())
        assertThat(call.args.warmupIterations.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.bundleManifest.first().toString().equals(this.bundleManifest) &&
            call.args.buildId.first().toString().equals(this.buildId) &&
            call.args.workload.first().toString().equals(this.workload) &&
            call.args.testIterations.first().toInteger().equals(this.testIterations.toInteger()) &&
            call.args.warmupIterations.first().toInteger().equals(this.warmupIterations.toInteger())
    }

    String libFunctionName() {
        return 'runPerfTestScript'
    }
}