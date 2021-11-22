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

    lib = library(identifier: 'jenkins@20211122', retriever: legacySCM(scm))
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifestLock))
    String shasRoot = inputManifest.getSHAsRoot("${JOB_NAME}", args.platform, args.architecture)

    buildManifest(
        args + [
            manifest: manifestLock
        ]
    )

    assembleManifest(
        args + [
            manifest: args.dryRun ? 'tests/data/opensearch-build-1.1.0.yml' : 'builds/manifest.yml'
        ]
    )

    uploadArtifacts(args)

    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        if (! args.dryRun) {
            s3Upload(bucket: "${ARTIFACT_BUCKET_NAME}", file: manifestLock, path: "${shasRoot}/${manifestSHA}.yml")
        } else {
            echo "s3Upload(bucket: ${ARTIFACT_BUCKET_NAME}, file: ${manifestLock}, path: ${shasRoot}/${manifestSHA}.yml)"
        }
    }
}
