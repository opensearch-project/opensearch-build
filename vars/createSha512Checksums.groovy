/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
Closure call() {
    allowedFileTypes = [".tar.gz", ".zip", ".rpm"]

    return { argsMap -> body: {

        final foundFiles = sh(script: "find ${argsMap.artifactPath} -type f", returnStdout: true).split()

        for (file in foundFiles) {
            acceptTypeFound = false
            for (fileType in allowedFileTypes) {
                if (file.endsWith(fileType)) {
                    echo("Creating sha for ${file}")
                    final sha512 = sh(script: "sha512sum ${file}", returnStdout: true).split()
                    //sha512 is an array [shasum, filename]
                    final basename = sh(script: "basename ${sha512[1]}", returnStdout: true)
                    // writing to file accroding to opensearch requirement - "512shaHash<space><space>basename"
                    writeFile file: "${file}.sha512", text: "${sha512[0]}  ${basename}"
                    acceptTypeFound = true
                    break
                }
            }
            if (!acceptTypeFound) {
                if(foundFiles.length == 1){
                    echo("Not generating sha for ${file} with artifact Path ${argsMap.artifactPath}, doesn't match allowed types ${allowedFileTypes}")
                } else {
                    echo("Not generating sha for ${file} in ${argsMap.artifactPath}, doesn't match allowed types ${allowedFileTypes}")
                }
            }
        }

    }}
}
