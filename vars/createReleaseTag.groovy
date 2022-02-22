def call(Map args = [:]) {

    def lib = library(identifier: 'jenkins@20211123', retriever: legacySCM(scm))
    def buildManifestObj = lib.jenkins.BuildManifest.new(readYaml(file: args.buildManifest))

    def componentsName = buildManifestObj.getComponets()
    def componetsNumber = componentsName.size()
    def version = args.tagVersion
    echo "Creating $version release tag for $componetsNumber components in ths manifest"

    withCredentials([usernamePassword(credentialsId: "${GITHUB_BOT_TOKEN_NAME}", usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
        for (component in componentsName) {
            def commitID = buildManifestObj.getCommitId(component)
            def repo = buildManifestObj.getRepo(component)
            def push_url = "https://$GITHUB_TOKEN@" + repo.minus('https://')
            echo "Tagging $component at $commitID ..."

            sh """
                mkdir $component
                cd $component
                git init
                git remote add origin $repo
                git fetch --depth 1 origin $commitID
                git checkout FETCH_HEAD
                if [ "$component" == "OpenSearch" ]; then
                    git tag $version
                else
                    git tag $version.0
                fi
                git push $push_url --tags
                cd ..
            """
        }
    }
}
