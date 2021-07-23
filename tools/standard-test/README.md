## OpenSearch/Dashboards IntegTest README

This folder contains all the necessary files and contents that are required to perform Integration Test (IntegTest) of plugins against
the OpenSearch/Dashboards bundled tarballs.

In the folder, you can find a script to deploy a single node cluster, a dockerfile to create an image for all the integTest environment,
two temporary scripts for mavenlocal deployment and bootstrap on dependencies (they will get removed once we have maven central), and a
nvm installation script from nvm github repo to help install nvm on the dockerfile.

### Requirements
* If you are using LINUX host to run dockerd, provision container based on the dockerfile, and execute integTest:
  * You must run these commands on the LINUX host for OpenSearch process to run:
    ```
    sudo sysctl -w vm.max_map_count=262144
    ulimit -n 65535
    ```

  * You must make this edit on the LINUX host and restart docker deamon for OpenSearch process to run.
    This will also prevent errors during Dashboards integtest (cypress) so that headless chrome will not crash.
    ```
    # Edit /etc/sysconfig/docker to have nofiles to 65535, and default shared memory to 1024MiB
    # OPTIONS="--default-ulimit nofile=65535:65535 --default-shm-size 1024000000"
    # Then restart docker
    sudo systemctl stop docker
    sudo systemctl start docker
    ```

* If you are using macOS host to run Docker Desktop, provision container based on the dockerfile, and execute integTest:
  * You must change docker memory/RAM utilization in resources settings if you use Docker Desktop on macOS.
    * Make sure at least 4GiB of RAM is used, so Dashboards process can startup correctly.

### Build docker image
* If you only want to build the docker image for either x64 or arm64, run this on a x64 or arm64 host respectively:
  ```
  docker build -f ./integtest-runner.al2.dockerfile . -t <Docker Hub RepoName>/<Docker Image Name>:<Tag Name>
  ```

* If you want to build multi-arch docker image for both x64 and arm64, make sure you are using Docker Desktop:
  * Run these commands to setup the multi-arch builder, you can re-use this build later on, just need to re-bootstrap again if you restart Docker Desktop:
    ```
    docker buildx create --name multiarch
    docker buildx use multiarch
    docker buildx inspect --bootstrap
    ```
  * You should be able to see similar output in `docker ps` like this:
    ```
    5907dc6dc16b moby/buildkit:buildx-stable-1 "buildkitd" 11 minutes ago Up 11 minutes buildx_buildkit_multiarch0
    ```
  * Docker buildx is using a container to build multi-arch images and combine all the layers together, so you can only upload it to Docker Hub,
    or save it locally as cache, means `docker images` will not show the image due to your host cannot have more than one CPU architecture.
  * Run these commands to actually build the docker image in multi-arch and push to Docker Hub (est. 1hr time depend on your host hardware specifications and network bandwidth):
    ```
    docker buildx build --platform linux/amd64,linux/arm64 -t <Docker Hub RepoName>/<Docker Image Name>:<Tag Name> --push .
    ```

### Run deployment script
* The deployment script is able to deploy a single node cluster with the specific version of OpenSearch/Dashboards bundle tarball on your host/container:
  * You must specify `-v VERSION`, `-t TYPE`, `-a ARCHITECTURE`, `-s ENABLE_SECURITY`
  * The script will attempt to download bundled tarball of OpenSearch/Dashboards from `artifacts.opensearch.org` and deploy to a temporary working directory.
  * Example:
    * Deploy OpenSearch/Dashboards 1.0.0 version, from snapshots channel, CPU arch x64, enable security:
    ```
    ./deploy_single_tar_cluster.sh -v 1.0.0 -t snapshots -a x64 -s true
    ```
    * Deploy OpenSearch/Dashboards 1.0.0 version, from releases channel, CPU arch arm64, disable security:
    ```
    ./deploy_single_tar_cluster.sh -v 1.0.0 -t releases -a arm64 -s false
    ```
  * The script allows in process wait and cleanup, meaning a `SIGINT / SIGTERM / SIGEXIT` or any child process throlwing `EXIT` signal will result in termination of the
    cluster as well as the temporary working directory.
  * If you want to run the deployment in detach mode, just run the command with `nohup <commands> &`.


