/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
Closure call() {

    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    return { args -> signArtifacts(args) }

}
