/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    // fileActions are a closure that accepts a String, filepath with return type void
    List<Closure> fileActions = args.fileActions ?: []

    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    String filename = inputManifest.build.getFilename()
    String version = inputManifest.build.version
    String qualifier = inputManifest.build.qualifier ? '-' + inputManifest.build.qualifier : ''
    String revision = version + qualifier
    println("Revision: ${revision}")

    List<String> distributionList = ["tar", "rpm"]

    for (distribution in distributionList) {

        // Must use local variable due to groovy for loop and closure scope
        // Or the stage will fixed to the last item in return when trigger new stages
        // https://web.archive.org/web/20181121065904/http://blog.freeside.co/2013/03/29/groovy-gotcha-for-loops-and-closure-scope/
        def distribution_local = distribution
        def artifactPath = "${DISTRIBUTION_JOB_NAME}/${revision}/${DISTRIBUTION_BUILD_NUMBER}/${DISTRIBUTION_PLATFORM}/${DISTRIBUTION_ARCHITECTURE}/${distribution_local}"
        def prefixPath = "${WORKSPACE}/artifacts/${distribution_local}"
        println("S3 download ${distribution_local} artifacts before creating signatures")

        withAWS(role: "${ARTIFACT_DOWNLOAD_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
            s3Download(bucket: "${ARTIFACT_BUCKET_NAME}", file: "${prefixPath}", path: "${artifactPath}/",  force: true)
        }

        String build_manifest = "$prefixPath/$artifactPath/builds/$filename/manifest.yml"
        def buildManifest = readYaml(file: build_manifest)

        print("Actions ${fileActions}")

        argsMap = [:]
        argsMap['sigtype'] = '.sig'

        String corePluginDir = "$prefixPath/$artifactPath/builds/$filename/core-plugins"
        boolean corePluginDirExists = fileExists(corePluginDir)

        //////////// Signing Artifacts
        println("Signing Starts")

        if(corePluginDirExists && distribution_local.equals('tar')) {
            println("Signing Core Plugins")
            argsMap['artifactPath'] = corePluginDir
            for (Closure action : fileActions) {
                action(argsMap)
            }
        }

        println("Signing Core/Bundle Artifacts")
        String coreFullPath = ['core', filename, revision].join('/')
        String bundleFullPath = ['bundle', filename, revision].join('/')
        for (Closure action : fileActions) {
            for (file in findFiles(glob: "**/${filename}-min-${revision}*.${distribution_local}*,**/${filename}-${revision}*.${distribution_local}*")) {
                argsMap['artifactPath'] = "$WORKSPACE" + "/" + file.getPath()
                action(argsMap)
            }
        }

        //////////// Uploading Artifacts
        withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
            // Core Plugins only needs to be published once through Tar, ignore other distributions
            if(corePluginDirExists && distribution_local.equals('tar')) {
                List<String> corePluginList = buildManifest.components.artifacts."core-plugins"[0]
                for (String pluginSubPath : corePluginList) {
                    String pluginSubFolder = pluginSubPath.split('/')[0]
                    String pluginNameWithExt = pluginSubPath.split('/')[1]
                    String pluginName = pluginNameWithExt.replace('-' + revision + '.zip', '')
                    String pluginNameNoExt = pluginNameWithExt.replace('-' + revision, '')
                    String pluginFullPath = ['plugins', pluginName, revision].join('/')
                    s3Upload(
                        bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}",
                        path: "releases/$pluginFullPath/",
                        workingDir: "$prefixPath/$artifactPath/builds/$filename/core-plugins/",
                        includePathPattern: "**/${pluginName}*"
                    )
                }
            }
            
            // We will only publish min artifacts for Tar, ignore other distributions
            if (distribution_local.equals('tar')) {
                s3Upload(
                    bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}",
                    path: "releases/$coreFullPath/",
                    workingDir: "$prefixPath/$artifactPath/builds/$filename/dist/",
                    includePathPattern: "**/${filename}-min-${revision}-${DISTRIBUTION_PLATFORM}-${DISTRIBUTION_ARCHITECTURE}*")
            }

            // We will publish bundle artifacts for all distributions
            s3Upload(
                bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}",
                path: "releases/$bundleFullPath/",
                workingDir: "$prefixPath/$artifactPath/dist/$filename/",
                includePathPattern: "**/${filename}-${revision}-${DISTRIBUTION_PLATFORM}-${DISTRIBUTION_ARCHITECTURE}*")

        }
    }
}
