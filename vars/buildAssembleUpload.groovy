void call(Map args = [:]) {
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"

    buildManifest(
        args + [
            manifest: manifest,
            lock: true
        ]
    )

    String manifestLock = args.dryRun ? manifest : "${manifest}.lock"
    manifestSHA = sha1(manifestLock)
    echo "Manifest SHA: ${manifestSHA}"

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifestLock))
    String shasRoot = inputManifest.getSHAsRoot("${JOB_NAME}", args.platform, args.architecture)
    String manifestShaPath = "${shasRoot}/${manifestSHA}.yml"

    Boolean shaExists = false
    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        if (!args.dryRun && s3DoesObjectExist(bucket: "${ARTIFACT_BUCKET_NAME}", path: manifestShaPath)) {
            shaExists = true
        }
    }

    if (shaExists) {
        lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Skipped ${STAGE_NAME}, ${manifestShaPath} exists.")
        echo "Skipping, ${manifestShaPath} already exists."
    } else {
        buildManifest(
            args + [
                manifest: manifestLock
            ]
        )

        assembleManifest(
            args + [
                manifest: args.dryRun ? 'tests/data/opensearch-build-1.1.0.yml' : "builds/${inputManifest.build.getFilename()}/manifest.yml"
            ]
        )

        uploadArtifacts(args)

        withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
            if (!args.dryRun) {
                s3Upload(bucket: "${ARTIFACT_BUCKET_NAME}", file: manifestLock, path: manifestShaPath)
            } else {
                echo "s3Upload(bucket: ${ARTIFACT_BUCKET_NAME}, file: ${manifestLock}, path: ${manifestShaPath})"
            }
        }

        String artifactUrl = inputManifest.getPublicDistUrl("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}", args.platform, args.architecture)
        echo "Setting env.\"ARTIFACT_URL_${args.platform}_${args.architecture}\"=${artifactUrl}"
        env."ARTIFACT_URL_${args.platform}_${args.architecture}" = artifactUrl
    }
}
