- [Building from Source](#building-from-source)
    - [OpenSearch](#opensearch)
    - [OpenSearch Dashboards](#opensearch-dashboards)
  - [Build Paths](#build-paths)
  - [Build.sh Options](#buildsh-options)
  - [Custom Build Scripts](#custom-build-scripts)
  - [Avoiding Rebuilds](#avoiding-rebuilds)

## Building from Source

The build workflow builds components declared in an input manifest from source, or downloads previously built artifacts, in order. All manifests for current releases are in [manifests](../../manifests). Here are some examples.

| name                                                                                 | description                                                    |
|--------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [opensearch-1.0.0.yml](/manifests/1.0.0/opensearch-1.0.0.yml)                        | Manifest to reproduce 1.0.0 build.                             |
| [opensearch-1.0.0-maven.yml](/manifests/1.0.0/opensearch-1.0.0-maven.yml)            | One-time manifest to build maven artifacts for 1.0 from tags.  |
| [opensearch-1.1.0.yml](/manifests/1.1.0/opensearch-1.1.0.yml)                        | Manifest for 1.1.0, the current version.                       |
| [opensearch-1.1.1.yml](/manifests/1.1.1/opensearch-1.1.1.yml)                        | Manifest for 1.1.1, a patch release.                           |
| [opensearch-1.2.0.yml](/manifests/1.2.0/opensearch-1.2.0.yml)                        | Manifest for 1.2.0, the next version.                          |
| [opensearch-2.0.0.yml](/manifests/2.0.0/opensearch-2.0.0.yml)                        | Manifest for 2.0.0, the next major version of OpenSearch.      |
| [opensearch-dashboards-1.1.0.yml](/manifests/1.1.0/opensearch-dashboards-1.1.0.yml)  | Manifest for 1.1.0, the next version of OpenSearch Dashboards. |    

The following example builds a snapshot version of OpenSearch 1.2.0.

```bash
./build.sh manifests/1.2.0/opensearch-1.2.0.yml --snapshot
```

While the following builds a snapshot version of OpenSearch-Dashboards 1.2.0.

```bash
./build.sh manifests/1.2.0/opensearch-dashboards-1.2.0.yml --snapshot
```

The [OpenSearch repo](https://github.com/opensearch-project/OpenSearch) is built first, followed by [common-utils](https://github.com/opensearch-project/common-utils), and all declared plugin repositories. These dependencies are published to maven local under `~/.m2`, and subsequent project builds pick those up. 

The [OpenSearch Dashboards repo](https://github.com/opensearch-project/OpenSearch-Dashboards) is built first, followed by all declared plugin repositories. 

All final output is placed into a `builds/opensearch` and `builds/opensearch-dashboards` folder respectively, along with a build output `manifest.yml` that contains output details.

#### OpenSearch

The build order first publishes `OpenSearch` followed by `common-utils`, and publishes these artifacts to maven local so that they are available for each component. In order to ensure that the same versions are used, a `-Dopensearch.version` flag is provided to each component's build script that defines which version the component should build against.

#### OpenSearch Dashboards

The build order first pulls down `OpenSearch-Dashboards` and then utilizes it to build other components. Currently, building plugins requires having the core repository built first to bootstrap and build the modules utilized by plugins.

### Build Paths

To build components we rely on a common entry-point in the form of a `build.sh` script. Within each build script components have the option to place artifacts in a set of directories to be picked up and published on their behalf. These are as follows.

| name               | description                                                                                             |
|--------------------|---------------------------------------------------------------------------------------------------------|
| /dist              | Include any distributions, e.g. opensearch or opensearch-dashboards min tarball.                        |
| /maven             | Include any publications that should be pushed to maven                                                 |
| /plugins           | Where a plugin zip should be placed. If included it will be installed during bundle assembly.           |
| /core-plugins      | Where plugins shipped from `https://github.com/opensearch-project/OpenSearch` should be placed          |
| /bundle            | Where the min bundle should be placed when built from `https://github.com/opensearch-project/OpenSearch`|
| /libs              | Where any additional libs should be placed that are required during bundle assembly                     |

### Build.sh Options

The following options are available in `build.sh`.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --snapshot         | Build a snapshot instead of a release artifact, default is `false`.     |
| --component [name] | Rebuild a single component by name, e.g. `--component common-utils`.    |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -l, --lock         | Generate a stable reference manifest.                                   |
| -v, --verbose      | Show more verbose output.                                               |

### Custom Build Scripts

Each component build relies on a `build.sh` script that is used to prepare bundle artifacts for a particular bundle version that takes two arguments: version and target architecture. By default the tool will look for a script in [scripts/components](../../scripts/components), then in the checked-out repository in `build/build.sh`, then default to a Gradle build implemented in [scripts/default/build.sh](../../scripts/default/build.sh).

### Avoiding Rebuilds

Builds can automatically generate a `manifest.lock` file with stable git references (commit IDs) and build options (platform, architecture and snapshot) by specifying `--lock`. The output can then be reused as input manifest after checking against a collection of prior builds.

```bash
MANIFEST=manifests/1.2.0/opensearch-1.2.0.yml
SHAS=shas

./build.sh --lock $MANIFEST # generates opensearch-1.2.0.yml.lock

MANIFEST_SHA=$(sha1sum $MANIFEST.lock | cut -f1 -d' ') # generate a checksum of the stable manifest

if test -f "$SHAS/$MANIFEST_SHA.lock"; then
  echo "Skipping $MANIFEST_SHA"
else
  ./build.sh $MANIFEST.lock # rebuild using stable references in .lock
  mkdir -p $SHAS
  cp $MANIFEST.lock $SHAS/$MANIFEST_SHA.lock # save the stable reference manifest
fi
```

The [Jenkins workflows](../../jenkins) in this repository can use this mechanism to avoid rebuilding all of OpenSearch and OpenSearch Dashboards unnecessarily. 
