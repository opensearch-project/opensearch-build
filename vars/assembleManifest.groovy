/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]) {
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))
    def filename = buildManifest.build.getFilename()
    def baseUrl = buildManifest.getArtifactRootUrlWithoutDistribution("${PUBLIC_ARTIFACT_URL}", "${JOB_NAME}", "${BUILD_NUMBER}")
    sh([
        './assemble.sh',
        "\"${args.buildManifest}\"",
        "--base-url ${baseUrl}"
    ].join(' '))

    if (buildManifest.build.distribution == 'rpm') {

        signArtifacts(
            artifactPath: "rpm/dist/${filename}",
            sigtype: '.rpm',
            platform: 'linux'
        )

        buildYumRepo(
            baseUrl: baseUrl,
            buildManifest: args.buildManifest
        )
    }
}
