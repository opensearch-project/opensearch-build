/**@
 * Copies a container from one docker registry to another
 *
 * @param args A map of the following parameters
 * @param args.imageRepository The repository of staging image. E.g.: opensearch, opensearch-dashboards, data-prepper
 * @param args.version The official version for release. E.g.: 2.0.1
 * @param args.sourceTag The image tag from the staging repo. E.g.: 2.0.1.3910
 * @param args.dockerPromote
 * @param args.ecrPromote
 * @param args.latestTag
 * @param args.majorVersionTag
 */
void call(Map args = [:]) {

    def imageRepo = args.imageRepository
    def version = args.version
    def sourceTag = args.sourceTag
    def dockerPromote = args.dockerPromote
    def ecrPromote = args.ecrPromote
    def latestBoolean = args.latestTag
    def majorVersionBoolean = args.majorVersionTag
    def majorVersion = version.split("\\.").first()

    //Promoting docker images
    if (dockerPromote) {
        println("Promoting to production docker hub with with $version tag.")
        copyContainer(
                sourceImage: "$imageRepo:$sourceTag",
                sourceRegistry: "opensearchstaging",
                destinationImage: "$imageRepo:$version",
                destinationRegistry: "opensearchproject"
        )
        if (majorVersionBoolean) {
            println("Promoting to production docker hub with with $majorVersion tag.")
            copyContainer(
                    sourceImage: "$imageRepo:$sourceTag",
                    sourceRegistry: "opensearchstaging",
                    destinationImage: "$imageRepo:$majorVersion",
                    destinationRegistry: "opensearchproject"
            )
        }
        if (latestBoolean) {
            println("Promoting to production docker hub with with latest tag.")
            copyContainer(
                    sourceImage: "$imageRepo:$sourceTag",
                    sourceRegistry: "opensearchstaging",
                    destinationImage: "$imageRepo:latest",
                    destinationRegistry: "opensearchproject"
            )
        }
    }
    if (ecrPromote) {
        println("Promoting to production ECR with with $version tag.")
        copyContainer(
                sourceImage: "$imageRepo:$sourceTag",
                sourceRegistry: "opensearchstaging",
                destinationImage: "$imageRepo:$version",
                destinationRegistry: "public.ecr.aws/opensearchproject"
        )
        if (majorVersionBoolean) {
            println("Promoting to production ECR with with $majorVersion tag.")
            copyContainer(
                    sourceImage: "$imageRepo:$sourceTag",
                    sourceRegistry: "opensearchstaging",
                    destinationImage: "$imageRepo:$majorVersion",
                    destinationRegistry: "public.ecr.aws/opensearchproject"
            )
        }
        if (latestBoolean) {
            println("Promoting to production ECR with with latest tag.")
            copyContainer(
                    sourceImage: "$imageRepo:$sourceTag",
                    sourceRegistry: "opensearchstaging",
                    destinationImage: "$imageRepo:latest",
                    destinationRegistry: "public.ecr.aws/opensearchproject"
            )
        }
    }

}