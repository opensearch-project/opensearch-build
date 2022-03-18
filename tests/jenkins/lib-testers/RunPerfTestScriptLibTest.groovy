import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat


class RunPerfTestScriptLibTester extends LibFunctionTester {

    private String bundleManifest
    private String buildId
    private String insecure
    private String workload
    private String testIterations
    private String warmupIterations

    public RunPerfTestScriptLibTester(bundleManifest, buildId, insecure, workload, testIterations, warmupIterations){
        this.bundleManifest = bundleManifest
        this.buildId = buildId
        this.insecure = insecure
        this.workload = workload
        this.testIterations = testIterations
        this.warmupIterations = warmupIterations
    }

    void configure(helper, binding) {
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })

        binding.setVariable('GITHUB_TOKEN', 'test_token')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'test_bucket')
        binding.setVariable('PERF_TEST_CONFIG_LOCATION', 'test_config')
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')

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
        return call.args.bundleManifest.first().toString().equals(this.bundleManifest)
                && call.args.buildId.first().toString().equals(this.buildId)
                && call.args.insecure.first().toString().equals(this.insecure)
                && call.args.workload.first().toString().equals(this.workload)
                && call.args.testIterations.first().toInteger().equals(this.testIterations.toInteger())
                && call.args.warmupIterations.first().toInteger().equals(this.warmupIterations.toInteger())
    }

    String libFunctionName() {
        return 'runPerfTestScript'
    }
}
