Closure call() {
    return { path -> body: {
        // Only create checksums for archive files
        if (path.endsWith(".tar.gz") || path.endsWith(".zip"))
            sh("sha512sum ${path} > ${path}.sha512")
        }
    }
}
