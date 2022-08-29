/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]) {
    String jobName = args.jobName ?: 'distribution-build-opensearch'
    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifest = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))
    String artifactRootUrl = buildManifest.getArtifactRootUrl(jobName, args.buildId)
    echo "Artifact root URL: ${artifactRootUrl}"

    String paths = generatePaths(buildManifest, artifactRootUrl)
    echo "Paths: ${paths}"

    sh([
        './test.sh',
        'bwc-test',
        "${args.testManifest}",
        "--test-run-id ${env.BUILD_NUMBER}",
        "--paths ${paths}",
    ].join(' '))
}

String generatePaths(buildManifest, artifactRootUrl) {
    String name = buildManifest.build.name
    return name == 'OpenSearch' ?
        "opensearch=${artifactRootUrl}" :
        "opensearch-dashboards=${artifactRootUrl}"
}
