void call(Map args = [:]){

    for(filename in args.artifactFileNames){
        println("File ${filename} can be accessed using the url - https://ci.opensearch.org/ci/dbc/${args.uploadPath}/${filename}" )
    }

}
