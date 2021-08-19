## Bundle Build

Builds the OpenSearch bundle.

This workflow contains two steps:

Step 1: Build

The OpenSearch repo is built first, followed by common-utils and all declared plugin repositories. These dependencies are published to maven
 local, and subsequent project builds pick those up. All final output is placed into an `artifacts` folder along with a `manifest.yml` that
  contains output details.
  Artifacts will contain the following folders:
  ```
  /artifacts
    bundle/ <- contains opensearch min tarball 
    maven/ <- all built maven artifacts
    plugins/ <- all built plugin zips
    manifest.yml <- Build manifest describing all built components and their artifacts.
  ```

Step 2: Bundle

The bundling step will take output from the build step and assemble a full bundle. The input requires a path to the build manifest and is
 expected to be inside the artifacts directory with the same directories.
All plugins built in step 1 will be installed and output to a `bundle` folder.
  ```
  /bundle
    <file-name>.tar.gz <- assembled tarball
    manifest.yml <- Bundle manifest describing versions for the min bundle and all installed plugins and their locations.
  ```

### Usage

Build Step:
```bash
./bundle-workflow/build.sh manifests/opensearch-1.0.0.yml
```

The following options are available.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| --snapshot         | Build a snapshot instead of a release artifact, default is `false`.     |
| --component [name] | Rebuild a single component by name, e.g. `--component common-utils`.    |
| --keep             | Do not delete the temporary working directory on both success or error. |

Bundle step:
```bash
./bundle-workflow/assemble.sh artifacts/manifest.yml
```
### Custom Build Scripts

Each component build relies on a `build.sh` script that is used to prepare bundle artifacts for a particular bundle version that takes two arguments: version and target architecture. By default the tool will look for a script in [scripts/components](scripts/components), then in the checked-out repository in `build/build.sh`, then default to a Gradle build implemented in [scripts/default/build.sh](scripts/default/build.sh).

#### Custom Install Scripts

You can perform additional plugin install steps by adding an `install.sh` script. By default the tool will look for a script in [scripts/components](scripts/components), then default to a noop version implemented in [scripts/default/install.sh](scripts/default/install.sh).