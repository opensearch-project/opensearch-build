
void call(Map args = [:]) {

    lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    assembleManifest(args)
    uploadArtifacts(args)
}