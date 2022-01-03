void call(Map args = [:]) {
    sh([
        './test.sh',
        'integ-test',
        "${args.testManifest}",
        "--paths opensearch=${args.artifactBasePath}",
        "--test-run-id ${env.BUILD_NUMBER}"
    ].join(' '))
}