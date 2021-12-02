void call(Map args = [:]) {
    sha = [
        sha: env."BUILD_SHA_${args.platform}_${args.architecture}_SHA",
        lock: env."BUILD_SHA_${args.platform}_${args.architecture}_LOCK",
        path: env."BUILD_SHA_${args.platform}_${args.architecture}_PATH"
    ]

    echo "Read BUILD_SHA_${args.platform}_${args.architecture}_[SHA|LOCK|PATH]."
    echo "sha.sha=${sha.sha}"
    echo "sha.lock=${sha.lock}"
    echo "sha.path=${sha.path}"

    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    if (sha.sha == null) {
        lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Skipped ${STAGE_NAME}, ${args.platform}-${args.architecture} was not built.")
        echo "Skipping, ${args.platform} ${args.architecture} was not built."
    } else {

        echo "Assembling ${sha.sha} (${sha.lock})"

        copyArtifacts(
            filter: "${sha.sha}-*.zip",
            fingerprintArtifacts: true,
            projectName: "${JOB_NAME}",
            selector: specific("${BUILD_NUMBER}")
        )

        unzip(zipFile: "${sha.sha}-builds.zip")
        unzip(zipFile: "${sha.sha}-manifest.zip")

        def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: sha.lock))

        assembleUpload(
            args + [
                manifest: "builds/${inputManifest.build.getFilename()}/manifest.yml",
                sha: sha
            ]
        )
    }
}
