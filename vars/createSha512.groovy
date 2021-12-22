Closure call() {
    allowedFileTypes = [".tar.gz", ".zip"]

    return { argsMap -> body: {

        //for (file in findFiles(glob: "**/$argsMap.artifactPath/*")) {
        //    acceptTypeFound = false
        //    println("file: " + file)

        //    for (fileType in allowedFileTypes) {
        //        println("fileType: " + fileType)
        //        if (file.endsWith(fileType)) {
        //            sh("sha512sum ${file} > ${file}.sha512")
        //            echo("Generating sha for ${file}")
        //            acceptTypeFound = true
        //            break
        //        }
        //    }

        //    if (!acceptTypeFound) {
        //        echo("Not generating sha for ${argsMap.artifactPath}, doesn't match allowed types ${allowedFileTypes}")
        //    }
        //}

        sh """
            set +x
            file_type_list=".tar.gz .zip"
            if [ -d "$argsMap.artifactPath" ]
            then
                for file_sub_path in `find $argsMap.artifactPath -type f`
                do
                    for file_type in \$file_type_list
                    do
                        if echo \$file_sub_path | grep -q \$file_type
                        then
                            echo Generating sha for \$file_sub_path
                            echo -ne `sha512sum \$file_sub_path | awk '{print $1}'` && echo -e "\t `basename \$file_sub_path`"
                        fi
                    done
                done
            else
               for file_type in \$file_type_list
               do
                   if echo $argsMap.artifactPath | grep -q \$file_type
                   then
                       echo Generating sha for $argsMap.artifactPath
                       echo -ne `sha512sum $argsMap.artifactPath | awk '{print $1}'` && echo -e "\t `basename $argsMap.artifactPath`"
                   fi
               done

            fi
        """

    }}
}
