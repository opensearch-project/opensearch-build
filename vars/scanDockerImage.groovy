void call(Map args = [:]) {

    sh """
        touch ${args.imageResultFile}.txt ${args.imageResultFile}.json
        trivy image --clear-cache
        trivy image --format table --output ${args.imageResultFile}.txt ${args.imageFullName}
        trivy image --format json --output ${args.imageResultFile}.json ${args.imageFullName}
    """

}
