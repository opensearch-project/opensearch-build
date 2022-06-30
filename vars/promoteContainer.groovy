/**@
 * Promote image from staging docker to production docker hub or ECR repository.
 *
 * @param args A map of the following parameters
 * @param args.imageRepository The repository of staging image. E.g.: opensearch:2.0.1.3910, opensearch-dashboards:2.0.1, data-prepper
 * @param args.version The official version for release. E.g.: 2.0.1
 * @param args.dockerPromote The boolean argument if promote containers from staging to production docker repo.
 * @param args.ecrPromote The boolean argument if promote containers from staging to production ECR repo.
 * @param args.latestTag The boolean argument if promote containers from staging to production with latest tag.
 * @param args.majorVersionTag The boolean argument if promote containers from staging to production with its major version tag.
 */
void call(Map args = [:]) {

    def imageRepo = args.imageRepository
    def version = args.version
    def imageProduct = imageRepo.split(':').first()
    def sourceTag = imageRepo.split(':').last()
    def dockerPromote = args.dockerPromote
    def ecrPromote = args.ecrPromote
    def latestBoolean = args.latestTag
    def majorVersionBoolean = args.majorVersionTag
    def majorVersion = version.split("\\.").first()

    def sourceReg = (imageRepo == 'data-prepper') ? ${DATA_PREPPER_STAGING_CONTAINER_REPOSITORY} : "opensearchstaging"
    def dockerProduction = "opensearchproject"
    def ecrProduction = "public.ecr.aws/opensearchproject"

    //Promoting docker images
    if (dockerPromote.toBoolean()) {
        println("Promoting $imageProduct to production docker hub with with $version tag.")
        copyContainer(
                sourceImage: "$imageProduct:$sourceTag",
                sourceRegistry: sourceReg,
                destinationImage: "$imageProduct:$version",
                destinationRegistry: dockerProduction
        )
        if (majorVersionBoolean.toBoolean()) {
            println("Promoting to production docker hub with with $majorVersion tag.")
            copyContainer(
                    sourceImage: "$imageProduct:$sourceTag",
                    sourceRegistry: sourceReg,
                    destinationImage: "$imageProduct:$majorVersion",
                    destinationRegistry: dockerProduction
            )
        }
        if (latestBoolean.toBoolean()) {
            println("Promoting to production docker hub with with latest tag.")
            copyContainer(
                    sourceImage: "$imageProduct:$sourceTag",
                    sourceRegistry: sourceReg,
                    destinationImage: "$imageProduct:latest",
                    destinationRegistry: dockerProduction
            )
        }
    }
    //Promoting image to ECR
    if (ecrPromote.toBoolean()) {
        println("Promoting to production ECR with with $version tag.")
        copyContainer(
                sourceImage: "$imageProduct:$sourceTag",
                sourceRegistry: sourceReg,
                destinationImage: "$imageProduct:$version",
                destinationRegistry: ecrProduction
        )
        if (majorVersionBoolean.toBoolean()) {
            println("Promoting to production ECR with with $majorVersion tag.")
            copyContainer(
                    sourceImage: "$imageProduct:$sourceTag",
                    sourceRegistry: sourceReg,
                    destinationImage: "$imageProduct:$majorVersion",
                    destinationRegistry: ecrProduction
            )
        }
        if (latestBoolean.toBoolean()) {
            println("Promoting to production ECR with with latest tag.")
            copyContainer(
                    sourceImage: "$imageProduct:$sourceTag",
                    sourceRegistry: sourceReg,
                    destinationImage: "$imageProduct:latest",
                    destinationRegistry: ecrProduction
            )
        }
    }
}
