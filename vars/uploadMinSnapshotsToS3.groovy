void call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    List<Closure> fileActions = args.fileActions ?: []
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"

    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    echo("Retreving build manifest from: $WORKSPACE/${args.distribution}/builds/${inputManifest.build.getFilename()}/manifest.yml")

    productName = inputManifest.build.getFilename()
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: "$WORKSPACE/${args.distribution}/builds/${productName}/manifest.yml"))
    version = buildManifest.build.version
    architecture = buildManifest.build.architecture
    platform = buildManifest.build.platform
    id = buildManifest.build.id
    extension = buildManifest.build.getExtension()

    // Setup src & dst variables for artifacts
    srcDir = "${WORKSPACE}/${args.distribution}/builds/${productName}/dist"
    dstDir = "snapshots/core/${productName}/${version}"
    baseName = "${productName}-min-${version}-${platform}-${architecture}"

    // Create checksums
    echo("Create .sha512 for Min Snapshots Artifacts")
    argsMap = [:]
    argsMap['artifactPath'] = srcDir
    for (Closure action : fileActions) { // running createSha512Checksums()
        action(argsMap)
    }

    sh """
        cp ${srcDir}/${baseName}.${extension} ${srcDir}/${baseName}-latest.${extension}
        cp ${srcDir}/${baseName}.${extension}.sha512 ${srcDir}/${baseName}-latest.${extension}.sha512
        sed -i "s/.${extension}/-latest.${extension}/g" ${srcDir}/${baseName}-latest.${extension}.sha512
    """
    withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(file: "${srcDir}/${baseName}-latest.${extension}", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "${dstDir}/${baseName}-latest.${extension}")
        s3Upload(file: "${srcDir}/${baseName}-latest.${extension}.sha512", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "${dstDir}/${baseName}-latest.${extension}.sha512")
    }
}
