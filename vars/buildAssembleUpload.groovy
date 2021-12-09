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

        assembleUpload(
            args + [
                manifest: "builds/${inputManifest.build.getFilename()}/manifest.yml",
                sha: sha
            ]
        )
    }
}
