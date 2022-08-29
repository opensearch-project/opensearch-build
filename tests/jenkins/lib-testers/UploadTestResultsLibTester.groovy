/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class UploadTestResultsLibTester extends LibFunctionTester {

    private String buildManifestFileName
    private String jobName
    private Integer buildNumber

    public UploadTestResultsLibTester(buildManifestFileName, jobName) {
        this.buildManifestFileName = buildManifestFileName
        this.jobName = jobName
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.buildManifestFileName.first(), notNullValue())
        assertThat(call.args.jobName.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.buildManifestFileName.first().toString().equals(this.buildManifestFileName)
                && call.args.jobName.first().toString().equals(this.jobName)
    }

    String libFunctionName() {
        return 'uploadTestResults'
    }

    void configure(helper, binding){
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_BUCKET_NAME')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'DUMMY_AWS_ACCOUNT_PUBLIC')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'DUMMY_ARTIFACT_BUCKET_NAME')
        binding.setVariable('PUBLIC_ARTIFACT_URL', 'DUMMY_PUBLIC_ARTIFACT_URL')
        binding.setVariable('env', ['BUILD_NUMBER': '487'])
        binding.setVariable('STAGE_NAME', 'DUMMY_STAGE_NAME')
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("s3Upload", [Map])
    }
}
