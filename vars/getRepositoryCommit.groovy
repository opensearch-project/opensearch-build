void call(Map args = [:]) {

    sh """#!/bin/bash

        set +x
        set -e

        COMPONENT_LIST=()
        COMPONENT_URL_LIST=()
        COMPONENT_REF_LIST=()

        mkdir -p commits; cd commits
        CURR_DIR=`pwd`
        OUTPUT_FILE=${args.outputFile}
        cp -v ${WORKSPACE}/${args.inputManifest} ${WORKSPACE}/\$OUTPUT_FILE

        if [ -z "${args.componentName}" ]; then
            echo "Component list not specified so search the entire input manifest: ${WORKSPACE}/${args.inputManifest}"
            read -r -a COMPONENT_LIST <<< `yq e '.components[].name' ${WORKSPACE}/${args.inputManifest} | tr '\n' ' '`
            echo "Component list: \${COMPONENT_LIST[@]}"
        else
            echo "Specified component list: ${args.componentName}"
            for comp in ${args.componentName}; do
                comp_temp=`yq e ".components[] | select(.name == \\"\$comp\\") | .name" ${WORKSPACE}/${args.inputManifest} | tr '\n' ' ' | head -n 1`
                if [ -z "\$comp_temp" ] || [ "\$comp_temp" = "null" ]; then
                    echo "ERROR: \$comp does not exist in manifest ${WORKSPACE}/${args.inputManifest}"
                    exit 1
                fi
            done
            read -r -a COMPONENT_LIST <<< "${args.componentName}"
            echo "Component list: \${COMPONENT_LIST[@]}"
        fi

        for entry in \${COMPONENT_LIST[@]}; do
            COMPONENT_URL_LIST+=(`yq e ".components[] | select(.name == \\"\$entry\\") | .repository" ${WORKSPACE}/${args.inputManifest} | tr '\n' ' ' | head -n 1`)
            COMPONENT_REF_LIST+=(`yq e ".components[] | select(.name == \\"\$entry\\") | .ref" ${WORKSPACE}/${args.inputManifest} | tr '\n' ' ' | head -n 1`)
        done

        echo "Component url list: \${COMPONENT_URL_LIST[@]}"
        echo "Component ref list: \${COMPONENT_REF_LIST[@]}"

        for index in \${!COMPONENT_LIST[@]}; do
            cd \$CURR_DIR
            mkdir -p \${COMPONENT_LIST[\$index]}
            cd \${COMPONENT_LIST[\$index]}
            git init -q
            git remote add origin \${COMPONENT_URL_LIST[\$index]}
            git fetch --depth 1 origin \${COMPONENT_REF_LIST[\$index]}
            git checkout -q FETCH_HEAD
            REAL_REF=`git rev-parse HEAD`
            echo \$REAL_REF
            yq -i ".components |= map(select(.name == \\"\${COMPONENT_LIST[\$index]}\\").ref=\\"\$REAL_REF\\")" ${WORKSPACE}/\$OUTPUT_FILE
        done
    """
}
