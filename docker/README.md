- [CI CD Environment](#ci-cd-environment)
  - [Build CI Runner Docker Image from Dockerfile](#build-ci-runner-docker-image-from-dockerfile)
  

## CI CD Environment

We build, assemble, and test our artifacts on docker containers. All of our pipelines are using the same docker image for consistency. This folder contains docker files in the [ci](./ci) folder, and images on [staging docker hub repositories](https://hub.docker.com/r/opensearchstaging/ci-runner/).

### Build CI Runner Docker Image from Dockerfile

If you only want to build the docker image for either x64 or arm64, run this on a x64 or arm64 host respectively:

```bash
docker build -f ./docker/ci/dockerfiles/integtest-runner.al2.dockerfile . -t <Docker Hub RepoName>/<Docker Image Name>:<Tag Name>
```

If you want to build multi-arch docker image for both x64 and arm64, make sure you are using Docker Desktop.

Run these commands to setup the multi-arch builder, you can re-use this build later on, just need to re-bootstrap again if you restart Docker Desktop.

```bash
docker buildx create --name multiarch
docker buildx use multiarch
docker buildx inspect --bootstrap
```

You should be able to see similar output in `docker ps` like this.

```
123456789012 moby/buildkit:buildx-stable-1 "buildkitd" 11 minutes ago Up 11 minutes buildx_buildkit_multiarch0
```

Docker buildx is using a container to build multi-arch images and combine all the layers together, so you can only upload it to Docker Hub, or save it locally as cache, means `docker images` will not show the image due to your host cannot have more than one CPU architecture.

Run these commands to actually build the docker image in multi-arch and push to Docker Hub (est. 1hr time depend on your host hardware specifications and network bandwidth).

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t <Docker Hub RepoName>/<Docker Image Name>:<Tag Name> -f <Docker File Path> --push .
```