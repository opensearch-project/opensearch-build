/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
void call(Map args = [:]){

    for(filename in args.artifactFileNames){
        url = "https://ci.opensearch.org/ci/dbc/${args.uploadPath}/${filename}"
        echo "File ${filename} can be accessed using the url - ${url}"
    }

}
