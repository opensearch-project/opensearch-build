Closure call() {
    allowedFileTypes = [".tar.gz", ".zip"]

    return { path -> body: {
        isAllowed = false
        for (fileType in allowedFileTypes) {
            isAllowed |= path.endsWith(fileType)
        }
        if (isAllowed) {
            sh("sha512sum ${path} > ${path}.sha512")
        } else {
            echo("Not generating sha for ${path}, doesn't match allowed types ${allowedFileTypes}")
        }
    } }
}
