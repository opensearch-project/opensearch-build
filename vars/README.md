- [Jenkins Shared Library](#jenkins-shared-library)
  - [Detecting Docker Agent](#detecting-docker-agent)
  - [All-In-One Build](#all-in-one-build)
  - [Cross-Platform Build](#cross-platform-build)
  - [Building Docker Images](#building-docker-images)
  - [Publishing Notifications](#publishing-notifications)
  - [Cleanup](#cleanup)
  - [Uploading Test Results](#uploading-test-results)

## Jenkins Shared Library

The Jenkins shared library implements common functions used by [Jenkins workflows](../jenkins) in this repository.

### Detecting Docker Agent

OpenSearch and OpenSearch Dashboards manifests contain a `ci` section with the docker image to use for building the manifest. This is loaded and published from [detectDockerAgent](./detectDockerAgent.groovy) to be used as `agent` arguments.

### All-In-One Build

A typical all-in-one build consists of [build](./buildManifest.groovy), [assemble](./assembleManifest.groovy) and [upload](./uploadArtifacts.groovy), implemented in [buildAssembleUpload.groovy](./buildAssembleUpload.groovy). This function also avoids rebuilds by generating a [SHA of the manifest lock](../README#avoiding-rebuilds) using [getManifestSHA](./getManifestSHA.groovy), and checking it against previously published artifacts.  

### Cross-Platform Build

A cross platform build divides the all-in-one build into steps that can be executed across multiple stages. For example, OpenSearch dashboards builds on an x64 docker image, but assembles on an arm64 docker image for an arm64 build.  

1. [buildArchive](./buildArchive.groovy) generates a manifest lock, calculates its SHA using [getManifestSHA](./getManifestSHA.groovy), and checks against previously built artifacts, before building and archiving the output to be used in a subsequent step. 
2. [archiveAssembleUpload](./archiveAssembleUpload.groovy) extracts previously archived build output and manifest lock, assembles a distribution and uploads it. 

### Building Docker Images

See [buildDockerImage](./buildDockerImage.groovy).

### Publishing Notifications

See [publishNotification](./publishNotification.groovy).

### Cleanup 

See [postCleanup](./postCleanup.groovy).

### Uploading Test Results

See [uploadTestResults](./uploadTestResults.groovy).
