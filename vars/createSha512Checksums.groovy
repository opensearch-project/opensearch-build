Closure call() {
    allowedFileTypes = [".tar.gz", ".zip"]

    return { argsMap -> body: {

        final foundFiles = sh(script: "find $argsMap.artifactPath -type f", returnStdout: true).split()

        for (file in foundFiles) {
            acceptTypeFound = false
            for (fileType in allowedFileTypes) {
                if (file.endsWith(fileType)) {
                    echo("Creating sha for ${file}")
                    final sha512 = sh(script: "sha512sum ${file}", returnStdout: true).split()
                    // Reading the first index of array since sha512sum return [shasum, filename] as output
                    writeFile file: "${file}.sha512", text: "${sha512[0]}"
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
