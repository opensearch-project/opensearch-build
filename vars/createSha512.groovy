Closure call() {
    allowedFileTypes = [".tar.gz", ".zip"]

    return { argsMap -> body: {
        isAllowed = false
        for (fileType in allowedFileTypes) {
            isAllowed |= argsMap.artifactPath.endsWith(fileType)
        }
        if (isAllowed) {
            sh("sha512sum ${argsMap.artifactPath} > ${argsMap.artifactPath}.sha512")
        } else {
            echo("Not generating sha for ${argsMap.artifactPath}, doesn't match allowed types ${allowedFileTypes}")
        }
    } }
}
