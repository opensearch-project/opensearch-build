void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def sha = getManifestSHA(args)

    if (sha.exists) {
        lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Skipped ${STAGE_NAME}, ${sha.path} exists.")
        echo "Skipping, ${sha.path} already exists."
    } else {

        def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: sha.lock))

        buildManifest(
            args + [
                manifest: sha.lock
            ]
        )

        assembleManifest(
            args + [
                manifest: args.dryRun ? 'tests/data/opensearch-build-1.1.0.yml' : "builds/${inputManifest.build.getFilename()}/manifest.yml"
            ]
        )

        uploadArtifacts(
            args + [
                manifest: args.dryRun ? 'tests/data/opensearch-build-1.1.0.yml' : "builds/${inputManifest.build.getFilename()}/manifest.yml"
            ]
        )

        withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
            if (!args.dryRun) {
                s3Upload(bucket: "${ARTIFACT_BUCKET_NAME}", file: sha.lock, path: sha.path)
            } else {
                echo "s3Upload(bucket: ${ARTIFACT_BUCKET_NAME}, file: ${sha.lock}, path: ${sha.path})"
            }
        }

        String artifactUrl = inputManifest.getPublicDistUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}", args.platform, args.architecture)
        echo "Setting env.\"ARTIFACT_URL_${args.platform}_${args.architecture}\"=${artifactUrl}"
        env."ARTIFACT_URL_${args.platform}_${args.architecture}" = artifactUrl
    }
}
