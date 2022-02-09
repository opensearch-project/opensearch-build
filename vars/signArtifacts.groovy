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
        sh """
            #!/bin/bash
            set +x
            export ROLE=${SIGNER_CLIENT_ROLE}
            export EXTERNAL_ID=${SIGNER_CLIENT_EXTERNAL_ID}
            export UNSIGNED_BUCKET=${SIGNER_CLIENT_UNSIGNED_BUCKET}
            export SIGNED_BUCKET=${SIGNER_CLIENT_SIGNED_BUCKET}

            $WORKSPACE/sign.sh ${arguments}
        """
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
