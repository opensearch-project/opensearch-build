/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import static org.hamcrest.CoreMatchers.notNullValue
import static org.hamcrest.MatcherAssert.assertThat
import static org.hamcrest.CoreMatchers.anyOf
import static org.hamcrest.CoreMatchers.equalTo

class DownloadFromS3LibTester extends LibFunctionTester {

    private String destPath
    private String bucket
    private String path
    private boolean force

    public DownloadFromS3LibTester(destPath, bucket, path, force){
        this.destPath = destPath
        this.bucket = bucket
        this.path = path
        this.force = force
    }

    void parameterInvariantsAssertions(call){
        assertThat(call.args.destPath.first(), notNullValue())
        assertThat(call.args.bucket.first(), notNullValue())
        assertThat(call.args.path.first(), notNullValue())
        assertThat(call.args.force.first(), notNullValue())
        assertThat(call.args.force.first().toString(), anyOf(equalTo('true'), equalTo('false')))
    }

    boolean expectedParametersMatcher(call) {
        return call.args.destPath.first().toString().equals(this.destPath)
                && call.args.bucket.first().toString().equals(this.bucket)
                && call.args.path.first().toString().equals(this.path)
                && call.args.force.first().toString().equals(this.force.toString())
    }

    String libFunctionName(){
        return 'downloadFromS3'
    }

    void configure(helper, binding){
        binding.setVariable('ARTIFACT_DOWNLOAD_ROLE_NAME', 'Dummy_Download_Role')
        binding.setVariable('AWS_ACCOUNT_PUBLIC', 'dummy_account')
        helper.registerAllowedMethod("s3Download", [Map])
        helper.registerAllowedMethod("withAWS", [Map, Closure], { args, closure ->
            closure.delegate = delegate
            return helper.callClosure(closure)
        })
    }
}
