/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

void call(Map args = [:]) {

    if( !fileExists("$WORKSPACE/sign.sh")) {
        git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
    }

    importPGPKey()

    // Sign artifacts
    withCredentials([usernamePassword(credentialsId: "${GITHUB_BOT_TOKEN_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
        sh """
            #!/bin/bash
            set +x
            export ROLE=${SIGNER_CLIENT_ROLE}
            export EXTERNAL_ID=${SIGNER_CLIENT_EXTERNAL_ID}
            export UNSIGNED_BUCKET=${SIGNER_CLIENT_UNSIGNED_BUCKET}
            export SIGNED_BUCKET=${SIGNER_CLIENT_SIGNED_BUCKET}

            $WORKSPACE/sign.sh ${args.artifactPath} --sigtype=${args.signatureType} --component=${args.component} --type=${args.type}
        """
    }
}

void importPGPKey(){
    if( !fileExists("$WORKSPACE/opensearch.pgp")) {
        sh("curl -SL https://artifacts.opensearch.org/publickeys/opensearch.pgp -o $WORKSPACE/opensearch.pgp")
        sh("gpg --import $WORKSPACE/opensearch.pgp")
    }
}
