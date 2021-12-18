Map call(Map args = [:]) {
    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))

    def buildManifest = lib.jenkins.BuildManifest.new(
        [
            name: args.name,
            version: args.version,
            platform: args.platform,
            architecture: args.architecture
        ]
    )

    return buildManifest.getArtifactRootUrl(args.jobName, args.buildNumber)
}
