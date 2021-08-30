- [OpenSearch Bundle Workflow](#opensearch-bundle-workflow)
    - [Build from Source](#build-from-source)
        - [Custom Build Scripts](#custom-build-scripts)
    - [Assemble the Bundle](#assemble-the-bundle)
        - [Custom Install Scripts](#custom-install-scripts)
    - [Signing Artifacts](#signing-artifacts)
    - [Test the Bundle](#test-the-bundle)
        - [Integration Tests](#integration-tests)
        - [Backwards Compatibility Tests](#backward-compatibility-tests)

## OpenSearch Bundle Workflow

This workflow builds a complete OpenSearch bundle from source. You can currently build 1.0, 1.1 and 1.1-SNAPSHOT.

### Build from Source

Each build requires a manifest to be passed as input.  We currently have the following input manifests:

| name        | description                                                                         |
|-------------|-------------------------------------------------------------------------------------|
| [opensearch-1.0.0.yml](/manifests/opensearch-1.0.0.yml) |  Manifest to reproduce 1.0.0 build.                 |
| [opensearch-1.0.0-maven.yml](/manifests/opensearch-1.0.0-maven.yml)|   One-time manifest to build and push maven artifacts for 1.0 from tags. Going forward a separate maven manifest is not required. For 1.0.0 we do not have solid 1.0 refs for all repos nor do we need to rebuild the full bundle.|
| [opensearch-1.1.0.yml](/manifests/opensearch-1.1.0.yml)| Manifest to build upcoming 1.x release.


Usage:
```bash
./bundle-workflow/build.sh manifests/opensearch-1.1.0.yml --snapshot
```

The [OpenSearch repo](https://github.com/opensearch-project/OpenSearch) is built first, followed by [common-utils](https://github.com/opensearch-project/common-utils), and all declared plugin repositories. These dependencies are published to maven local under `~/.m2`, and subsequent project builds pick those up. All final output is placed into an `artifacts` folder along with a build output `manifest.yml` that contains output details.

Artifacts will contain the following folders.

```
/artifacts
  bundle/ <- contains opensearch min tarball 
  maven/ <- all built maven artifacts
  plugins/ <- all built plugin zips
  core-plugins/ <- all built core plugins zip
  manifest.yml <- build manifest describing all built components and their artifacts
```

The following options are available in `bundle-workflow/build.sh`.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --snapshot         | Build a snapshot instead of a release artifact, default is `false`.     |
| --component [name] | Rebuild a single component by name, e.g. `--component common-utils`.    |
| --keep             | Do not delete the temporary working directory on both success or error. |

#### Custom Build Scripts

Each component build relies on a `build.sh` script that is used to prepare bundle artifacts for a particular bundle version that takes two arguments: version and target architecture. By default the tool will look for a script in [scripts/components](scripts/components), then in the checked-out repository in `build/build.sh`, then default to a Gradle build implemented in [scripts/default/build.sh](scripts/default/build.sh).

### Assemble the Bundle 

```bash
./bundle-workflow/assemble.sh artifacts/manifest.yml
```

The bundling step takes output from the build step, installs plugins, and assembles a full bundle into a `bundle` folder. The input requires a path to the build manifest and is expected to be inside the `artifacts` directory that contains `bundle`, `maven`, `plugins` and `core-plugins` subdirectories from the build step.

Artifacts will be updated as follows.

```
/bundle
  <file-name>.tar.gz <- assembled tarball
  manifest.yml <- bundle manifest describing versions for the min bundle and all installed plugins and their locations
```

#### Custom Install Scripts

You can perform additional plugin install steps by adding an `install.sh` script. By default the tool will look for a script in [scripts/bundle-build/components](scripts/bundle-build/components), then default to a noop version implemented in [scripts/default/install.sh](scripts/default/install.sh).

### Signing Artifacts

The signing step (optional) takes the manifest file created from the build step and signs all its component artifacts using the opensearch-signer-client. The input requires a path to the build manifest and is expected to be inside the artifacts directory with the same directories mentioned in the build step. 

The following options are available. 

| name        | description                                                                         |
|-------------|-------------------------------------------------------------------------------------|
| --component | The component name of the component whose artifacts will be signed                  |
| --type      | The artifact type to be signed. Currently one of 3 options: [plugins, maven, bundle]|

The signed artifacts (<artifact>.asc) will be found in the same location as the original artifact. 

Signing step (to sign all artifacts):
```bash
./bundle_workflow/sign.sh artifacts/manifest.yml
```

### Test the Bundle
Tests the OpenSearch bundle.

This workflow contains two sections: Integration Tests, Backwards Compatibility Tests.

#### Integration Tests
This step runs integration tests invoking `integtest.sh` in each component from bundle manifest.

#### Backwards Compatibility Tests
This step run backward compatibility invoking `bwctest.sh` in each component from bundle manifest.

Usage:

Kick off all test suites on a manifest:
```bash
./bundle-workflow/test.sh manifests/opensearch-1.0.0.yml
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --component [name] | Test a single component by name, e.g. `--component common-utils`.    |
| --keep             | Do not delete the temporary working directory on both success or error. |
