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

        echo "Archiving into ${sha.sha} zip: builds/**, ${sha.lock}"

        zip(
            zipFile: "${sha.sha}-builds.zip",
            archive: true,
            glob: 'builds/**'
        )

        zip(
            zipFile: "${sha.sha}-manifest.zip",
            archive: true,
            glob: sha.lock
        )

        lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Built ${STAGE_NAME}, ${sha.sha}.")

        def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: sha.lock))
        echo "Setting env.BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_SHA=${sha.sha}"
        env."BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_SHA" = sha.sha
        echo "Setting env.BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_LOCK=${sha.lock}"
        env."BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_LOCK" = sha.lock
        echo "Setting env.BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_PATH=${sha.path}"
        env."BUILD_SHA_${inputManifest.build.platform}_${inputManifest.build.architecture}_PATH" = sha.path
    }
}
