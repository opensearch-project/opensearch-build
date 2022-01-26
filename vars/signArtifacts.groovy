/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

/*
This library will take in arguments Map with only these options as Keys [artifactPath, component, type, signatureType, distributionPlatform] with case-sensitive
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
    // artifactPath is mandatory and the first argument
    String arguments = args.artifactPath
    // generation command line arguments
    args.each{key, value -> !key.equals("artifactPath") ? arguments += " --${key}=${value}" : ""}
    return arguments
}

void importPGPKey(){

    sh "curl -sSL https://artifacts.opensearch.org/publickeys/opensearch.pgp | gpg --import -"

}
