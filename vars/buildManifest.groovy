/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]) {
    sh(([
        './build.sh',
        args.inputManifest ?: "manifests/${INPUT_MANIFEST}",
        args.distribution ? "-d ${args.distribution}" : null,
        args.componentName ? "--component ${args.componentName}" : null,
        args.platform ? "-p ${args.platform}" : null,
        args.architecture ? "-a ${args.architecture}" : null,
        args.snapshot ? '--snapshot' : null,
        args.lock ? '--lock' : null
    ] - null).join(' '))
}
