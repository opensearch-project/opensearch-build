/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    buildManifest(args)

    String stashName = "${args.stashName}"
    echo "Stashing builds to assemble later with name: ${stashName}"
    stash includes: "${args.distribution}/builds/**", name: "${stashName}"

    lib.jenkins.Messages.new(this).add("${STAGE_NAME}", "Built ${STAGE_NAME}.")

}
