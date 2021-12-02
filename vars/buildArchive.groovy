void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def sha = getManifestSHA(args)

    if (sha.exists) {
        lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Skipped ${STAGE_NAME}, ${sha.path} exists.")
        echo "Skipping, ${sha.path} already exists."
    } else {

        buildManifest(
            args + [
                manifest: sha.lock
            ]
        )

        zip(
            zipFile: "${sha.sha}.zip",
            archive: false,
            glob: './builds/**/*'
        )

        archiveArtifacts(
            artifacts: "${sha.sha}.zip,${sha.path},${sha.lock}",
            fingerprint: true
        )

        def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: sha.lock))
        echo "Setting env.BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_SHA=${sha.sha}"
        env."BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_SHA" = sha.sha
        echo "Setting env.BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_LOCK=${sha.lock}"
        env."BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_LOCK" = sha.lock
        echo "Setting env.BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_PATH=${sha.path}"
        env."BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_PATH" = sha.path
    }
}
