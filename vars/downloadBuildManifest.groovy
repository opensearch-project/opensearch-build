/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
def call(Map args = [:]) {
    def lib = library(identifier: "jenkins@20211123", retriever: legacySCM(scm))

    sh "curl -sSL ${args.url} --output ${args.path}"
    def buildManifestObj = lib.jenkins.BuildManifest.new(readYaml(file: args.path))
    return buildManifestObj
}
