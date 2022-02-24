### Summary
We support building OpenSearch and OpenSearch Dashboards docker for both [multi-CPU](https://docs.docker.com/desktop/multi-arch/) and single CPU architectures.
Users are welcome to choose either type of the image to build on their local development environment, or directly pulling existing images published on Docker Hub:

[OpenSearch Docker Repository](https://hub.docker.com/r/opensearchproject/opensearch/)

[OpenSearch-Dashboards Docker Repository](https://hub.docker.com/r/opensearchproject/opensearch-dashboards/)

```
docker pull opensearchproject/opensearch:latest
docker pull opensearchproject/opensearch-dashboards:latest
```

### Building Docker Images
#### We provide two scripts to build docker images. For single-arch image you need to install just the Docker Engine on your host machine. For multi-arch image (currently support x64/arm64) you need to install Docker Desktop (macOS/Windows) or Docker Buildx (LINUX).

Install Docker through the official docker webpage: https://docs.docker.com/get-docker/


After installation, verify if you have Docker Engine by running:
  ```
  docker build --help
  ```


Verify if you have Docker Desktop or Docker Buildx Standalone by running:
  ```
  docker buildx --help
  ```


You need to run both script within the `opensearch-build/docker/release` folder. Running them
  within other path would cause the scripts to fail.

#### Build single-arch image with these commands:
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
#### Build multi-arch image with this commands (only support x64 + arm64 in one image for now), the image will immediately uploaded to a docker registry so you need to provide docker repo name:
  * OpenSearch 1.0.0:
    ```
    ./build-image-multi-arch.sh -v 1.0.0 -f ./dockerfiles/opensearch.al2.dockerfile -p opensearch -a "x64,arm64" -r "<Docker Hub RepoName>/<Docker Image Name>:<Tag Name>"
    ```
  * OpenSearch-Dashboards 1.0.0 with local tarball(s):
    ```
    ./build-image-multi-arch.sh -v 1.0.0 -f ./dockerfiles/opensearch-dashboards.al2.dockerfile -p opensearch-dashboards -a "x64,arm64" -r "<Docker Hub RepoName>/<Docker Image Name>:<Tag Name>" -t "opensearch-1.0.0.tar.gz,opensearch-dashboards-1.0.0.tar.gz"
    ```

### Disable Security Plugin, Security Dashboards Plugin, Security Demo Configurations and Related Configurations
(This change is added since OpenSearch/OpenSearch-Dashboards 1.1.0)
There are 3 environment variables available for users to disable security related settings during docker container startup:

* 2 for OpenSearch:
  * __DISABLE_INSTALL_DEMO_CONFIG__: Default to `null`, set to `true` disables running of [install_demo_configuration.sh](https://github.com/opensearch-project/security/blame/main/tools/install_demo_configuration.sh) bundled with Security Plugin, which installs demo certificates and security configurations to OpenSearch.
  * __DISABLE_SECURITY_PLUGIN__: Default to `null`, set to `true` disables Security Plugin entirely in OpenSearch by setting `plugins.security.disabled: true` in opensearch.yml.

* 1 for Dashboards:
  * __DISABLE_SECURITY_DASHBOARDS_PLUGIN__: Default to `null`, set to `true` disables Security Dashboards Plugin in OpenSearch-Dashboards by removing securityDashboards plugin folder, remove all related settings in opensearch_dashboards.yml, and set `opensearch.hosts` entry protocol from HTTPS to HTTP. This step is not reversible as the Security Dashboards Plugin is removed in the process. If you want to re-enable security for OpenSearch-Dashboards, you need to start a new container with `DISABLE_SECURITY_DASHBOARDS_PLUGIN` unset, or false.


Here are three example scenarios of using above variables:

#### Scenario 1: Original behavior, install demo certs/configs + enable security on both OpenSearch and OpenSearch-Dashboards:
  * OpenSearch:
     ```
     $ docker run -it -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:1.1.0
     ```
  * OpenSearch-Dashboards:
     ```
     $ docker run -it --network="host" opensearchproject/opensearch-dashboards:1.1.0
     ```

#### Scenario 2: No demo certs/configs + disable security on both OpenSearch and OpenSearch-Dashboards:
  * OpenSearch:
     ```
     $ docker run -it -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "DISABLE_INSTALL_DEMO_CONFIG=true" -e "DISABLE_SECURITY_PLUGIN=true" opensearchproject/opensearch:1.1.0
     ```
  * OpenSearch-Dashboards:
     ```
     $ docker run -it --network="host" -e "DISABLE_SECURITY_DASHBOARDS_PLUGIN=true" opensearchproject/opensearch-dashboards:1.1.0
     ```

#### Scenario 3: No demo certs/configs + enable security on both OpenSearch and OpenSearch-Dashboards (cluster exit with errors due to demo install script is not run. Therefore, no certs/configs are available for Security Plugin. Useful if you want to setup your own certs/configs):
  * OpenSearch:
     ```
     $ docker run -it -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "DISABLE_INSTALL_DEMO_CONFIG=true" opensearchproject/opensearch:1.1.0
     ```
  * Dashboards:
     ```
     $ docker run -it --network="host" -e opensearchproject/opensearch-dashboards:1.1.0
     ```

