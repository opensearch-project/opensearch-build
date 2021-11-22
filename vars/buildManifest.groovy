void call(Map args = [:]) {
    sh (([
        args.dryRun ? 'echo ./build.sh' : './build.sh',
        args.manifest ?: "manifests/${INPUT_MANIFEST}",
        args.platform ? "-p ${args.platform}" : null,
        args.architecture ? "-a ${args.architecture}" : null,
        args.snapshot ? '--snapshot' : null,
        args.lock ? '--lock' : null
    ] - null).join(' '))
}
