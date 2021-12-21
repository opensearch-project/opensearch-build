void call(Map args = [:]) {

    environment {
        // These ENV variables are required by https://github.com/opensearch-project/opensearch-signer-client
        // This client is invoked internally by the sign script.
        ROLE = "${SIGNER_CLIENT_ROLE}"
        EXTERNAL_ID = "${SIGNER_CLIENT_EXTERNAL_ID}"
        UNSIGNED_BUCKET = "${SIGNER_CLIENT_UNSIGNED_BUCKET}"
        SIGNED_BUCKET = "${SIGNER_CLIENT_SIGNED_BUCKET}"
    }

    if( !fileExists("$WORKSPACE/sign.sh")) {
        git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
    }

    if( !fileExists("$WORKSPACE/opensearch.pgp")) {
        sh('curl https://artifacts.opensearch.org/publickeys/opensearch.pgp -o $WORKSPACE/opensearch.pgp')
        sh('gpg --import $WORKSPACE/opensearch.pgp')
    }

    // Sign artifacts
    withCredentials([usernamePassword(credentialsId: "${GITHUB_BOT_TOKEN_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
        sh("$WORKSPACE/sign.sh $WORKSPACE/${args.artifactPath} --sigType=${args.signatureType} --component=${args.component} --type=${args.type}")
    }
}
