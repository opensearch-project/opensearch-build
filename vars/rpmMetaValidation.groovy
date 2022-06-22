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

    // Validate the distribution signature
    def checksig = sh (
            script: "rpm -K -v $distFile",
            returnStdout: true
    ).trim()
    println("Signature check of the rpm distribution file is: \n" + checksig)
    def keyList = ["Header V4 RSA/SHA512 Signature, key ID 9310d3fc", "Header SHA256 digest",
                   "Header SHA1 digest", "Payload SHA256 digest",
                   "V4 RSA/SHA512 Signature, key ID 9310d3fc", "MD5 digest"]
    def presentKey = []
    for (line in checksig.split('\n')) {
        def key = line.split(':')[0].trim()
        if (key == distFile) {
            continue
        } else {
            assert line.split(':', 2)[1].trim().contains("OK")
            println(key + " is validated as: " + line)
            presentKey.add(key)
        }
    }
    println("Validation all key digests starts: ")
    for (digest in keyList) {
        assert presentKey.contains(digest)
        println("Key digest \"$digest\" is validated to be present.")
    }
    println("Validation for signature of RPM distribution completed.")
}
