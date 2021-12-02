Map call(Map args = [:]) {
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"

    buildManifest(
        args + [
            manifest: manifest,
            lock: true
        ]
    )

    String manifestLock = args.dryRun ? manifest : "${manifest}.lock"
    String manifestSHA = sha1(manifestLock)
    echo "Manifest SHA: ${manifestSHA}"

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifestLock))
    String shasRoot = inputManifest.getSHAsRoot("${JOB_NAME}", args.platform, args.architecture)
    String manifestSHAPath = "${shasRoot}/${manifestSHA}.yml"

    Boolean manifestSHAExists = false
    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        if (s3DoesObjectExist(bucket: "${ARTIFACT_BUCKET_NAME}", path: manifestSHAPath)) {
            manifestSHAExists = true
        }
    }

    return [
        sha: manifestSHA,
        lock: manifestLock,
        path: manifestSHAPath,
        exists: manifestSHAExists
    ]
}
