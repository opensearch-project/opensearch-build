#!/bin/bash

set -e

# Import libs
. ../../lib/shell/file_management.sh

# Variable
OLDIFS=$IFS
BUILDER_NUM=`date +%s`
BUILDER_NAME="multiarch_${BUILDER_NUM}"
DIR=""

function usage() {
    echo ""
    echo "This script is used to build the OpenSearch Docker image with single architecture (x64 or arm64). It prepares the files required by the Dockerfile in a temporary directory, then builds and tags the Docker image."
    echo "--------------------------------------------------------------------------"
    echo "Usage: $0 [args]"
    echo ""
    echo "Required arguments:"
    echo -e "-v VERSION\tSpecify the OpenSearch version number that you are building, e.g. '1.0.0' or '1.0.0-beta1'. This will be used to label the Docker image. If you do not use the '-o' option then this tool will download a public OPENSEARCH release matching this version."
    echo -e "-f DOCKERFILE\tSpecify the dockerfile full path, e.g. dockerfile/opensearch.al2.dockerfile."
    echo -e "-p PRODUCT\tSpecify the product, e.g. opensearch or opensearch-dashboards, make sure this is the name of your config folder and the name of your .tgz defined in dockerfile."
    echo -e "-a ARCHITECTURE\tSpecify the multiple architecture you want to add to the multi-arch image, separate by comma, e.g. 'x64,arm64'."
    echo -e "-r REPOSITORY\tSpecify the docker repository name in the format of '<Docker Hub RepoName>/<Docker Image Name>:<Tag Name>', due to multi-arch image either save in cache or directly upload to Docker Hub Repo, no local copies."
    echo ""
    echo "Optional arguments:"
    echo -e "-o TARBALL\tSpecify multiple opensearch or opensearch-dashboards tarballs, use the same order as the input for '-a' param, e.g. 'opensearch-1.0.0-linux-x64.tar.gz,opensearch-1.0.0-linux-arm64.tar.gz'. You still need to specify the version - this tool does not attempt to parse the filename."
    echo -e "-h\t\tPrint this message."
    echo "--------------------------------------------------------------------------"
}

function cleanup_docker_buildx() {
    # Cleanup docker buildx
    echo -e "\n* Cleanup docker buildx"
    docker buildx use default
    docker buildx rm $BUILDER_NAME > /dev/null 2>&1
}

function cleanup_all() {
    cleanup_docker_buildx
    File_Delete $DIR
}
while getopts ":ho:v:f:p:a:r:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        o)
            TARBALL=`realpath $OPTARG`
            ;;
        v)
            VERSION=$OPTARG
            ;;
        f)
            DOCKERFILE=$OPTARG
            ;;
        p)
            PRODUCT=$OPTARG
            ;;
        a)
            ARCHITECTURE=$OPTARG
            ;;
        r)
            REPOSITORY=$OPTARG
            ;;
        :)
            echo "-${OPTARG} requires an argument"
            usage
            exit 1
            ;;
        ?)
            echo "Invalid option: -${arg}"
            exit 1
            ;;
    esac
done

# Validate the required parameters to present
if [ -z "$VERSION" ] || [ -z "$DOCKERFILE" ] || [ -z "$PRODUCT" ] || [ -z "$ARCHITECTURE" ]; then
  echo "You must specify '-v VERSION', '-f DOCKERFILE', '-p PRODUCT', '-a ARCHITECTURE'"
  usage
  exit 1
else
  echo $VERSION $DOCKERFILE $PRODUCT $ARCHITECTURE
  IFS=', ' read -r -a ARCHITECTURE_ARRAY <<< "$ARCHITECTURE"
  IFS=', ' read -r -a TARBALL_ARRAY <<< "$TARBALL"
fi

# Warning docker desktop
if (! docker buildx version)
then
    echo -e "\n* You MUST have Docker Desktop to use buildx for multi-arch images."
    exit 1
fi

# Prepare docker buildx
trap cleanup_all TERM INT EXIT
DIR=`Temp_Folder_Create`
echo New workspace $DIR
echo -e "\n* Prepare docker buildx"
docker buildx use default
docker buildx create --name $BUILDER_NAME --use
docker buildx inspect --bootstrap

# Check buildx status
echo -e "\n* Check buildx status"
docker buildx ls | grep $BUILDER_NAME
docker ps | grep $BUILDER_NAME


# Copy configs
cp -v config/${PRODUCT}/* $DIR/
cp -v ../../scripts/opensearch-onetime-setup.sh $DIR/

# Copy TGZ
if [ -z "$TARBALL" ]; then
    for index1 in ${!ARCHITECTURE_ARRAY[@]}
    do
        # No tarball file specified so download one
        URL="https://artifacts.opensearch.org/releases/bundle/${PRODUCT}/${VERSION}/${PRODUCT}-${VERSION}-linux-${ARCHITECTURE_ARRAY[$index1]}.tar.gz"
        echo -e "\nDownloading ${PRODUCT} arch ${ARCHITECTURE_ARRAY[$index1]} version ${VERSION} from ${URL}"
        curl -f $URL -o ${DIR}/${PRODUCT}-${ARCHITECTURE_ARRAY[$index1]}.tgz || exit 1
    done
    ls -l $DIR
else
    for index2 in ${!ARCHITECTURE_ARRAY[@]}
    do
        echo -e "\nCopying ${PRODUCT} arch ${ARCHITECTURE_ARRAY[$index1]} version ${VERSION} from ${TARBALL_ARRAY[$index2]}"
        cp -v ${TARBALL_ARRAY[$index2]} ${DIR}/${PRODUCT}-${ARCHITECTURE_ARRAY[$index2]}.tgz
    done
    ls -l $DIR
fi

# Build multi-arch images
PLATFORMS=`echo "${ARCHITECTURE_ARRAY[@]/#/linux/}" | sed 's/x64/amd64/g;s/ /,/g'` && echo PLATFORMS $PLATFORMS
docker buildx build --platform $PLATFORMS --build-arg VERSION=$VERSION --build-arg ARCHITECTURE=$ARCHITECTURE --build-arg BUILD_DATE=`date -u +%Y-%m-%dT%H:%M:%SZ` -t $REPOSITORY -f $DOCKERFILE --push .

