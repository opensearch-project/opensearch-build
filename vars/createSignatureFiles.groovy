Closure call() {

    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    return { args -> signArtifacts(args) }

}
