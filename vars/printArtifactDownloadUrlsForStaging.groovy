void call(Map args = [:]){

    for(filename in args.artifactFileNames){
        url = "https://ci.opensearch.org/ci/dbc/${args.uploadPath}/${filename}"
        println("File ${filename} can be accessed using the url - ${url}" )
    }

}
