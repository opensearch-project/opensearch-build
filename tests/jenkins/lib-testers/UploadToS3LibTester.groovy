/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat

class UploadToS3LibTester extends LibFunctionTester {

    private String sourcePath
    private String bucket
    private String path

    public UploadToS3LibTester(sourcePath, bucket, path){
        this.sourcePath = sourcePath
        this.bucket = bucket
        this.path = path
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.sourcePath.first(), notNullValue())
        assertThat(call.args.bucket.first(), notNullValue())
        assertThat(call.args.path.first(), notNullValue())
    }

    boolean expectedParametersMatcher(call) {
        return call.args.sourcePath.first().toString().equals(this.sourcePath)
                && call.args.bucket.first().toString().equals(this.bucket)
                && call.args.path.first().toString().equals(this.path)
    }

    String libFunctionName(){
        return 'uploadToS3'
    }

    void configure(helper, binding){
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        binding.setVariable('ARTIFACT_BUCKET_NAME', 'dummy_bucket_name')
        helper.registerAllowedMethod("s3Upload", [Map])
        helper.registerAllowedMethod("withCredentials", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }
}
