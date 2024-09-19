The distribution workflow builds a complete OpenSearch and OpenSearch Dashboards distribution from source. This system performs a top-down [build](https://github.com/opensearch-project/opensearch-build/tree/main/src/build_workflow) of all components required for a specific OpenSearch and OpenSearch Dashboards release, then [assembles](https://github.com/opensearch-project/opensearch-build/tree/main/src/assemble_workflow/) a distribution. The input to the system is a manifest that defines the order in which components should be built. All manifests for our current releases are placed in [manifests folder](https://github.com/opensearch-project/opensearch-build/tree/main/manifests). For older versions, please see [legacy-manifests](https://github.com/opensearch-project/opensearch-build/tree/main/legacy-manifests) folder.
  
### What are manifests?
Before we start to build, let's understand what is manifest and the types of manifest that you will come across. 
Manifests are the single source of truth for building and testing the distributions. There are 3 types of manifest, each with a difference schema.
  
* **_Input Manifest_** : As the name suggests, input manifest is the starting point and source of building OpenSearch and OpenSearch Dashboard distributions. See the [schema](https://github.com/opensearch-project/opensearch-build/blob/main/src/manifests/input_manifest.py#L13-L39) of the input manifest. This manifest consist of CI docker image that contains all the dependencies to build an OpenSearch and OpenSearch Dashboard distribution. It also contains the components' GitHub repository URLs, reference to build, basic CI checks as well as platforms the components supports. 
  
* **_Build Manifest_** : Build Manifest is the interim manifest that is generated after components are built. See the [schema](https://github.com/opensearch-project/opensearch-build/blob/main/src/manifests/build_manifest.py#L17-L42) for build manifest. You can find those manifests in `builds` folder locally. This manifest contains interim artifacts such as zips, libraries, maven artifacts, etc. See sample [build manifest](https://github.com/opensearch-project/opensearch-build/blob/main/tests/data/opensearch-build-2.0.0-rc1.yml).
  
* **_Distribution Manifest_** : Distribution manifest, as the name suggests is the final manifest bundles with the distribution. See the [schema](https://github.com/opensearch-project/opensearch-build/blob/main/src/manifests/bundle_manifest.py#L15-L36) for the distribution manifest. This manifest contains all the information about a distribution and the components bundled in that distribution. 
  
### Building from Source
  
Input manifests are the source of building the distributions. Each input manifest also contains the docker image that can be used to build these distributions and avoid installing bunch of packages. See [CI image details](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/3.0.0/opensearch-3.0.0.yml#L8-L9) in the manifest.
  
To run locally:
```bash
  docker run -it -d --entrypoint bash opensearchstaging/ci-runner:ci-runner-centos7-opensearch-build-v2 -e JAVA_HOME=/opt/java/openjdk-20
```
Then build from source:
  
```bash
./build.sh manifests/3.0.0/opensearch-3.0.0.yml 
```

Additional arguments:

```
optional arguments:
  -h, --help            show this help message and exit
  -l, --lock            Generate a stable reference manifest.
  -s, --snapshot        Build snapshot.
  -c [COMPONENTS ...], --component [COMPONENTS ...]
                        Rebuild one or more components.
  --keep                Do not delete the working temporary directory.
  -p {linux,darwin,windows}, --platform {linux,darwin,windows}
                        Platform to build.
  -a {x64,arm64}, --architecture {x64,arm64}
                        Architecture to build.
  -v, --verbose         Show more verbose output.
  -d {tar,zip,rpm,deb}, --distribution {tar,zip,rpm,deb}
                        Distribution to build.
```
  
This builds OpenSearch 3.0.0 from source, placing the output into `./builds/opensearch`. 
  
See [build workflow](https://github.com/opensearch-project/opensearch-build/tree/main/src/build_workflow) for more information.
  
### Assembling a Distribution 
  
Assembling a distribution needs build manifest as an input.
  
```bash
./assemble.sh builds/opensearch/manifest.yml
```
  
The assembling step takes output from the build step, installs plugins, and assembles a full distribition into the `dist` folder. 
  
See [assemble workflow](https://github.com/opensearch-project/opensearch-build/tree/main/src/assemble_workflow) for more information.
  
### Building Patches
  
A patch release contains output from previous versions mixed with new source code. Manifests can mix such references. See [opensearch-1.3.1.yml](/manifests/1.3.1/opensearch-1.3.1.yml) for an example.
  
OpenSearch is often released with changes in `opensearch-min`, and no changes to plugins other than a version bump. This can be performed by a solo Engineer following [a cookbook](https://github.com/opensearch-project/opensearch-plugins/blob/main/META.md#increment-a-version-in-every-plugin). See also [opensearch-build#1375](https://github.com/opensearch-project/opensearch-build/issues/1375) which aims to automate incrementing versions for the next development iteration.
  
#### CI/CD Environment
  
We use Jenkins as our CI/CD infrastructure to build, test and release OpenSearch and OpenSearch Dashboards. Access it [here](https://build.ci.opensearch.org/)
  
We build, assemble, and test our artifacts on docker containers. We provide docker files in [docker/ci](https://github.com/opensearch-project/opensearch-build/tree/main/docker/ci) folder, and images on [staging docker hub repositories](https://hub.docker.com/r/opensearchstaging/ci-runner/). All Jenkins pipelines can be found in [jenkins](https://github.com/opensearch-project/opensearch-build/tree/main/jenkins). The Jenkins is deployed using infrastructure as a Code and can be found in [opensearch-ci](https://github.com/opensearch-project/opensearch-ci) repository.
  
See [jenkins](https://github.com/opensearch-project/opensearch-build/tree/main/jenkins) and [docker](https://github.com/opensearch-project/opensearch-build/tree/main/docker) for more information.
  
#### Build Numbers
  
The distribution url and the build output manifest include a Jenkins auto-incremented build number. For example, the [manifest](https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.2.0/5905/linux/x64/rpm/dist/opensearch/manifest.yml) from [OpenSearch build 5905](https://build.ci.opensearch.org/job/distribution-build-opensearch/5905/) contains the following.
  
```yml
build:
  name: OpenSearch
  version: 2.2.0
  platform: linux
  architecture: x64
  distribution: rpm
  id: '5905'
```

### Where to find the nightly artifacts?

Below are the details where you can find the nighly artifacts build for OpenSearch and OpenSearch-Dashboards distribution. 
Please note that since these nightly artifacts, they are not recommended for production use.

#### OpenSearch-Min Snapshots
  
Snapshots for OpenSearch core/min can be downloaded and used in CI's, local development, etc using below links:
  
Linux:
```
https://artifacts.opensearch.org/snapshots/core/opensearch/<version>-SNAPSHOT/opensearch-min-<version>-SNAPSHOT-linux-x64-latest.tar.gz
```
Macos:
```
https://artifacts.opensearch.org/snapshots/core/opensearch/<version>-SNAPSHOT/opensearch-min-<version>-SNAPSHOT-darwin-x64-latest.tar.gz
```
  
Windows:
```
https://artifacts.opensearch.org/snapshots/core/opensearch/<version>-SNAPSHOT/opensearch-min-<version>-SNAPSHOT-windows-x64-latest.zip
```

#### Latest Distributions Builds
  
Use the `latest` keyword in the URL to obtain the latest nightly build for a given version. For example https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.12.0/latest/linux/x64/rpm/dist/opensearch/manifest.yml redirects to [build 9234](https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.12.0/9234/linux/x64/rpm/dist/opensearch/manifest.yml) at the time of writing this.
  
The `latest` keyword is resolved to a specific build number by checking an `index.json` [file](https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.12.0/index/linux/x64/tar/index.json). This file is maintained individually for each platform, architecture and distribution. The index.json file has contents similar to

```
{"latest":"9445"}
```

The resolution logic is implemented in the [CloudFront URL rewriter](https://github.com/opensearch-project/opensearch-ci/tree/main/resources/cf-url-rewriter). 
The TTL (time to live) is set to `5 mins` which means that the `latest` url may need up to 5 mins to get new contents after `index.json` is updated.
  
All the artifacts accessible through the regular distribution URL can be accessed by the `latest` URL. This includes both OpenSearch Core, OpenSearch Dashboards Core and their plugins. 
  
For example, you can download the latest .tar.gz distribution build of OpenSearch 2.12.0 directly at https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.12.0/latest/linux/x64/tar/dist/opensearch/opensearch-2.12.0-linux-x64.tar.gz, without having to first download and parse the [complete build manifest](https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.12.0/latest/linux/x64/tar/dist/opensearch/manifest.yml).
  
For plugin artifacts, you can also use the `latest` keyword to get the latest plugin artifacts with a known version. E.g. in order to get performance-analyzer x64 tarball artifacts for 2.1.0, you can obtain it with link https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.1.0/latest/linux/x64/tar/builds/opensearch/plugins/opensearch-performance-analyzer-2.1.0.0.zip, which will redirect you to https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.1.0/5757/linux/x64/tar/builds/opensearch/plugins/opensearch-performance-analyzer-2.1.0.0.zip.
  
For bundled artifacts, here are some examples for LINUX and Windows:
* Linux Tar: https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.4.0/latest/linux/x64/tar/dist/opensearch/opensearch-2.4.0-linux-x64.tar.gz
* Windows Zip: https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.4.0/latest/windows/x64/zip/dist/opensearch/opensearch-2.4.0-windows-x64.zip

#### Docker images

The nightly build docker images are published to [opensearchstaging](https://hub.docker.com/u/opensearchstaging) account with version tag.

See [OpenSearch](https://hub.docker.com/r/opensearchstaging/opensearch/tags) and [OpenSearch-Dashboards](https://hub.docker.com/r/opensearchstaging/opensearch-dashboards/tags) images. 
