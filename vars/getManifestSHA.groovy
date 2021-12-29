Map call(Map args = [:]) {
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    String jobName = args.jobName ?: "${JOB_NAME}"

    buildManifest(
        args + [
            manifest: manifest,
            lock: true
        ]
    )

    String manifestLock = "${manifest}.lock"
    String manifestSHA = sha1(manifestLock)
    echo "Manifest SHA: ${manifestSHA}"

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifestLock))
    String shasRoot = inputManifest.getSHAsRoot(jobName)
    String manifestSHAPath = "${shasRoot}/${manifestSHA}.yml"
    echo "Manifest lock: ${manifestLock}"
    echo "Manifest SHA path: ${manifestSHAPath}"

    Boolean manifestSHAExists = false
    withAWS(role: 'opensearch-bundle', roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        if (s3DoesObjectExist(bucket: "${ARTIFACT_BUCKET_NAME}", path: manifestSHAPath)) {
            manifestSHAExists = true
        }
    }

    echo "Manifest SHA exists: ${manifestSHAExists}"

    return [
        sha: manifestSHA,
        lock: manifestLock,
        path: manifestSHAPath,
        exists: manifestSHAExists
    ]
}
