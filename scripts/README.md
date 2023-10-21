- [Scripts](#scripts)
    - [Run Deployment Script](#run-deployment-script)
      - [Requirements](#requirements)
      - [Usage](#usage)
  
## Scripts

This folder contains default and custom scripts located by [src/paths/script_finder.py](../src/paths/script_finder.py), and the following scripts which are used in either tar/docker or legacy github actions.

#### Run Deployment Script

This is a script to deploy a single node OpenSearch + OpenSearch-Dashboards cluster to a x64 or arm64 host.

##### Requirements

* If you are using LINUX host to run dockerd, provision container based on the dockerfile, and execute integTest:
  * You must run these commands on the LINUX host for OpenSearch process to run:
    ```
    sudo sysctl -w vm.max_map_count=262144
    ulimit -n 65535
    ```

  * You must make this edit on the LINUX host and restart docker daemon for OpenSearch process to run.
    This will also prevent errors during Dashboards integtest (cypress) so that headless chrome will not crash.
    * Option 1 (Recommended):
      ```
      # Edit /etc/docker/daemon.json with these changes:
      {
        "default-ulimits": {
          "nofile": {
            "Hard": 65535,
            "Name": "nofile",
            "Soft": 65535
          }
        },
        "default-shm-size": "1024M"
      }
      # Then restart docker
      sudo systemctl stop docker
      sudo systemctl start docker
      ```
    * Option 2:
      ```
      # If you have /etc/sysconfig/docker on your LINUX host
      # Edit /etc/sysconfig/docker to have nofiles to 65535, and default shared memory to 1024MiB
      # OPTIONS="--default-ulimit nofile=65535:65535 --default-shm-size 1024000000"
      # Then restart docker
      sudo systemctl stop docker
      sudo systemctl start docker
      ```

##### Usage

* If you are using macOS host to run Docker Desktop, provision container based on the dockerfile, and execute integTest:
  * You must change docker memory/RAM utilization in resources settings if you use Docker Desktop on macOS.
    * Make sure at least 4GiB of RAM is used, so Dashboards process can startup correctly.

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
  * The script allows in process wait and cleanup, meaning a `SIGINT / SIGTERM / SIGEXIT` or any child process throwing `EXIT` signal will result in termination of the
    cluster as well as the temporary working directory.
  * If you want to run the deployment in detach mode, just run the command with `nohup <commands> &`.


