void call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    List<Closure> fileActions = args.fileActions ?: []
    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"

    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    echo("Retreving build manifest from: $WORKSPACE/builds/${inputManifest.build.getFilename()}/manifest.yml")

    productName = inputManifest.build.getFilename()
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: "$WORKSPACE/builds/${productName}/manifest.yml"))
    version = buildManifest.build.version
    architecture = buildManifest.build.architecture
    platform = buildManifest.build.platform
    id = buildManifest.build.id

    // Setup src & dst variables for artifacts
    srcDir = "${WORKSPACE}/builds/${productName}/dist"
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
        cp ${srcDir}/${baseName}.tar.gz ${srcDir}/${baseName}-latest.tar.gz
        cp ${srcDir}/${baseName}.tar.gz.sha512 ${srcDir}/${baseName}-latest.tar.gz.sha512
        sed -i "s/.tar.gz/-latest.tar.gz/g" ${srcDir}/${baseName}-latest.tar.gz.sha512
    """
    withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Upload(file: "${srcDir}/${baseName}-latest.tar.gz", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "${dstDir}/${baseName}-latest.tar.gz")
        s3Upload(file: "${srcDir}/${baseName}-latest.tar.gz.sha512", bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "${dstDir}/${baseName}-latest.tar.gz.sha512")
    }
}
