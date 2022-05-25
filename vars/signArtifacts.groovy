/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

/*
SignArtifacts signs the given artifacts and saves the signature in the same directory
@param Map[artifactPath] <Required> - Path to yml or artifact file.
@param Map[component] <Optional> - Path to yml or artifact file.
@param Map[type] <Optional> - Artifact type in the manifest, [type] is required for signing yml.
@param Map[sigtype] <Optional> - The signature type of signing artifacts. e.g. '.sig'. Required for non-yml artifacts signing.
@param Map[platform] <Required> - The distribution platform for signing.
*/
void call(Map args = [:]) {

    if( !fileExists("$WORKSPACE/sign.sh")) {
        git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
    }

    importPGPKey()
    
    String arguments = generateArguments(args)


    // Sign artifacts
    withCredentials([usernamePassword(credentialsId: "${GITHUB_BOT_TOKEN_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
        def configSecret = args.platform == "windows" ? "signer-windows-config" : "signer-pgp-config"
        withCredentials([string(credentialsId: configSecret, variable: 'configs')]) {
            def creds = readJSON(text: configs)
            def ROLE = creds['role']
            def EXTERNAL_ID = creds['external_id']
            def UNSIGNED_BUCKET = creds['unsigned_bucket']
            def SIGNED_BUCKET = creds['signed_bucket']
            def PROFILE_IDENTIFIER = creds['profile_identifier']
            def PLATFORM_IDENTIFIER = creds['platform_identifier']
            sh """
                #!/bin/bash
                set +x
                export ROLE=$ROLE
                export EXTERNAL_ID=$EXTERNAL_ID
                export UNSIGNED_BUCKET=$UNSIGNED_BUCKET
                export SIGNED_BUCKET=$SIGNED_BUCKET
                export PROFILE_IDENTIFIER=$PROFILE_IDENTIFIER
                export PLATFORM_IDENTIFIER=$PLATFORM_IDENTIFIER
    
                $WORKSPACE/sign.sh ${arguments}
            """
        }
    }
}

String generateArguments(args) {
    String artifactPath = args.remove("artifactPath")
    // artifactPath is mandatory and the first argument
    String arguments = artifactPath
    // generation command line arguments
    args.each{key, value -> arguments += " --${key}=${value}"}
    return arguments
}

void importPGPKey(){

    sh "curl -sSL https://artifacts.opensearch.org/publickeys/opensearch.pgp | gpg --import -"

}
