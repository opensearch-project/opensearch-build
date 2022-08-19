void call(Map args = [:]) {
    sh(([
        './build.sh',
        args.inputManifest ?: "manifests/${INPUT_MANIFEST}",
        args.distribution ? "-d ${args.distribution}" : null,
        args.componentName ? "--component ${args.componentName}" : null,
        args.platform ? "-p ${args.platform}" : null,
        args.architecture ? "-a ${args.architecture}" : null,
        args.snapshot ? '--snapshot' : null,
        args.lock ? '--lock' : null
    ] - null).join(' '))
}
