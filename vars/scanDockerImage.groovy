/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]) {

    sh """
        touch ${args.imageResultFile}.txt ${args.imageResultFile}.json
        trivy image --clear-cache
        trivy image --format table --output ${args.imageResultFile}.txt ${args.imageFullName}
        trivy image --format json --output ${args.imageResultFile}.json ${args.imageFullName}
    """

}
