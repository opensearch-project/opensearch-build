String call(String repository) {
    if (!repository) {
        throw new IllegalArgumentException("repository property was not set, try again with getRepositoryName('fooRepository')")
    }
    afterLastSlash = repository.tokenize("/").pop()
    onlyRepoName = afterLastSlash.tokenize(".")[0]

    return onlyRepoName
}