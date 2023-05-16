- [CI CD Environment](#ci-cd-environment)
  - [Build CI Runner Docker Image from Dockerfile](#build-ci-runner-docker-image-from-dockerfile)
  

## CI CD Environment

We build, assemble, and test our artifacts on docker containers. All of our pipelines are using the same docker image for consistency. This folder contains docker files in the [ci](./ci) folder, and images on [staging docker hub repositories](https://hub.docker.com/r/opensearchstaging/ci-runner/).

### Build CI Runner Docker Image from Dockerfile

To build the docker image for either x64 or arm64, run the below command on a x64 or arm64 host respectively within the `opensearch-build/docker/ci` folder:

```bash
./build-image-single-arch.sh -r <Repo Name> -v <Tag Name> -f <Docker File Path>
```
After the build, you can locate an image in your host using the `docker images` command with the following format: `opensearchstaging/<Repo Name>:<Tag Name>`.


If you want to build multi-arch docker image for both x64 and arm64, you can use the below command.\
Make sure you are running it within the `opensearch-build/docker/ci` folder.

```bash
./build-image-multi-arch.sh -r <Repo Name> -v <Tag Name> -f <Docker File Path>
```
Docker buildx is a tool utilized for building multi-arch images. It leverages a `moby/buildkit` container to construct these images, combining all the CPU architecture layers into a single entity. Consequently, you can only upload the resulting image to Docker Hub or store it locally as cache. Due to the limitation that your host cannot support multiple CPU architectures, the image will not be visible when running the `docker images` command.

