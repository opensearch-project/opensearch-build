/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

void call(Map args = [:]) {
    git url: 'https://github.com/opensearch-project/opensearch-build.git', branch: 'main'
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    String manifest = args.manifest ?: "manifests/${INPUT_MANIFEST}"
    def inputManifest = lib.jenkins.InputManifest.new(readYaml(file: manifest))
    String filename = inputManifest.build.getFilename()
    String version = inputManifest.build.version

    def artifactPath = "${DISTRIBUTION_JOB_NAME}/${version}/${DISTRIBUTION_BUILD_NUMBER}/${DISTRIBUTION_PLATFORM}/${DISTRIBUTION_ARCHITECTURE}"

    withAWS(role: "${ARTIFACT_DOWNLOAD_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_PUBLIC}", duration: 900, roleSessionName: 'jenkins-session') {
        s3Download(bucket: "${ARTIFACT_BUCKET_NAME}", file: "$WORKSPACE/artifacts", path: "${artifactPath}/",  force: true)
    }

    String build_manifest = "artifacts/$artifactPath/builds/$filename/manifest.yml"
    def buildManifest = readYaml(file: build_manifest)

    withAWS(role: "${ARTIFACT_PROMOTION_ROLE_NAME}", roleAccount: "${AWS_ACCOUNT_ARTIFACT}", duration: 900, roleSessionName: 'jenkins-session') {
        // Core Plugins
        println("Start Core Plugin Promotion to artifects.opensearch.org Bucket")
        List<String> corePluginList = buildManifest.components.artifacts."core-plugins"[0]
        for (String pluginSubPath : corePluginList) {
            String pluginSubFolder = pluginSubPath.split('/')[0]
            String pluginNameWithExt = pluginSubPath.split('/')[1]
            String pluginName = pluginNameWithExt.replace('-' + version + '.zip', '')
            String pluginFullPath = ['plugins', pluginName, version].join('/')
            s3Upload(bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "releases/$pluginFullPath/", workingDir: "$WORKSPACE/artifacts/$artifactPath/builds/$filename/$pluginSubFolder/"
                , includePathPattern: "**/${pluginName}*")
        }


        // Tar Core/Bundle
        println("Start Tar Core/Bundle Promotion to artifacts.opensearch.org Bucket")
        String coreFullPath = ['core', filename, version].join('/')
        String bundleFullPath = ['bundle', filename, version].join('/')
        s3Upload(bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "releases/$coreFullPath/", workingDir: "$WORKSPACE/artifacts/$artifactPath/builds/$filename/dist/"
                , includePathPattern: "**/${filename}-min-${version}*")
        s3Upload(bucket: "${ARTIFACT_PRODUCTION_BUCKET_NAME}", path: "releases/$bundleFullPath/", workingDir: "$WORKSPACE/artifacts/$artifactPath/dist/$filename/"
                , includePathPattern: "**/${filename}*-${version}*")


    }

}
