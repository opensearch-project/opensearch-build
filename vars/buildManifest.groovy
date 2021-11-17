void call(Map args = [:]) {
    sh (([
        args.script ?: './build.sh',
        args.manifest ?: "manifests/${INPUT_MANIFEST}",
        args.platform ? "-p ${args.platform}" : null,
        args.architecture ? "-a ${args.architecture}" : null,
        args.snapshot ? "--snapshot" : null
    ] - null).join(' '))
}
