## OpenSearch/Dashboards Docker Build README

### Summary
We support building OpenSearch/Dashboards docker images with [multi-CPU architecture support](https://docs.docker.com/desktop/multi-arch/).
We also support old school single CPU architecture build as well.
Users are welcome to choose either type of the image to build on their local development environment, or directly pulling existing images published on Docker Hub:

[OpenSearch Docker Repository](https://hub.docker.com/r/opensearchproject/opensearch/)

[OpenSearch-Dashboards Docker Repository](https://hub.docker.com/r/opensearchproject/opensearch-dashboards/)

```
docker pull opensearchproject/opensearch:latest
docker pull opensearchproject/opensearch-dashboards:latest
```

### Building docker images 
We provide two scripts to build docker images.
For single-arch image you need to install just the Docker Engine on your host machine.
For multi-arch image (currently support x64/arm64) you need to install Docker Desktop.

* Install Docker through the official docker webpage: https://docs.docker.com/get-docker/

* After installation, verify whether or not you have Docker Engine by running:
  ```
  docker build --help
  ```

* Verify if you have Docker Desktop by running:
  ```
  docker buildx --help
  ```

* You need to run both script within the `opensearch-build/release/docker` folder. Running them
  within other path would cause the scripts to fail.

* Build single-arch image with these command:
  * OpenSearch 1.0.0 x64:
    ```
    ./build-image-single-arch.sh -v 1.0.0 -f ./dockerfiles/opensearch.al2.dockerfile -p opensearch -a x64
    ```
  * OpenSearch 1.0.0 arm64 with local tarball:
    ```
    ./build-image-single-arch.sh -v 1.0.0 -f ./dockerfiles/opensearch.al2.dockerfile -p opensearch -a arm64 -t opensearch-1.0.0.tar.gz
    ```
  * OpenSearch-Dashboards 1.0.0 x64:
    ```
    ./build-image-single-arch.sh -v 1.0.0 -f ./dockerfiles/opensearch-dashboards.al2.dockerfile -p opensearch-dashboards -a x64
    ```
  * OpenSearch-Dashboards 1.0.0 arm64 with local tarball:
    ```
    ./build-image-single-arch.sh -v 1.0.0 -f ./dockerfiles/opensearch-dashboards.al2.dockerfile -p opensearch-dashboards -a arm64 -t opensearch-dashboards-1.0.0.tar.gz
    ```
* Build multi-arch image with this commands (only support x64 + arm64 in one image for now), the image will immediately uploaded to a docker registry so you need to provide docker repo name:
  * OpenSearch 1.0.0:
  ```
  ./build-image-multi-arch.sh -v 1.0.0 -f ./dockerfiles/opensearch.al2.dockerfile -p opensearch -a "x64,arm64" -r "<Docker Hub RepoName>/<Docker Image Name>:<Tag Name>"
  ```
  * OpenSearch-Dashboards 1.0.0 with local tarball(s):
  ```
  ./build-image-multi-arch.sh -v 1.0.0 -f ./dockerfiles/opensearch-dashboards.al2.dockerfile -p opensearch-dashboards -a "x64,arm64" -r "<Docker Hub RepoName>/<Docker Image Name>:<Tag Name>" -t "opensearch-1.0.0.tar.gz,opensearch-dashboards-1.0.0.tar.gz"
  ```
