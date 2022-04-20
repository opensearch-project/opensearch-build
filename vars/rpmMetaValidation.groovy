/**
 * This is a general function for RPM distribution validation.
 * @param Map args = [:]
 * args.refMap: The Map contains the expected meta data from the Manifest.
 * args.rpmDistribution: The location of the RPM distribution file.
 */
def call(Map args = [:]) {

    def distFile = args.rpmDistribution
    def refMap = args.refMap

    //Validation for the Meta Data of distribution
    println("Meta data validations start:")
    def metadata = sh (
            script: "rpm -qip $distFile",
            returnStdout: true
    ).trim()
    println("Meta data for the RPM distribution is: \n" + metadata)
    // Extract the meta data from the distribution to Map
    def metaMap = [:]
    for (line in metadata.split('\n')) {
        def key = line.split(':')[0].trim()
        if (key != 'Description') {
            metaMap[key] = line.split(':', 2)[1].trim()
        } else {
            metaMap[key] = metadata.split(line)[1].trim()
            break
        }
    }
    // Start validating
    refMap.each{ key, value ->
        if (key == "Architecture") {
            if (value == 'x64') {
                assert metaMap[key] == 'x86_64'
            } else if (value == 'arm64') {
                assert metaMap[key] == 'aarch64'
            }
        } else {
            assert metaMap[key] == value
        }
        println("Meta data for $key is validated")
    }
    println("Validation for meta data of RPM distribution completed.")
}
