- [OpenSearch Bundle Workflow](#opensearch-bundle-workflow)
    - [Build from Source](#build-from-source)
        - [Custom Build Scripts](#custom-build-scripts)
    - [Assemble the Bundle](#assemble-the-bundle)
        - [Custom Install Scripts](#custom-install-scripts)

## OpenSearch Bundle Workflow

### Build from Source

```bash
./bundle-workflow/build.sh manifests/opensearch-1.0.0.yml
```

The [OpenSearch repo](https://github.com/opensearch-project/OpenSearch) is built first, followed by [common-utils](https://github.com/opensearch-project/common-utils), and all declared plugin repositories. These dependencies are published to maven local under `~/.m2`, and subsequent project builds pick those up. All final output is placed into an `artifacts` folder along with a build output `manifest.yml` that contains output details.

Artifacts will contain the following folders.

```
/artifacts
  bundle/ <- contains opensearch min tarball 
  maven/ <- all built maven artifacts
  plugins/ <- all built plugin zips
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

The bundling step takes output from the build step, installs plugins, and assembles a full bundle into a `bundle` folder. The input requires a path to the build manifest and is expected to be inside the `artifacts` directory that contains `bundle`, `maven` and `plugins` subdirectories from the build step.

Artifacts will be updated as follows.

```
/bundle
  <file-name>.tar.gz <- assembled tarball
  manifest.yml <- bundle manifest describing versions for the min bundle and all installed plugins and their locations
```

#### Custom Install Scripts

You can perform additional plugin install steps by adding an `install.sh` script. By default the tool will look for a script in [scripts/bundle-build/components](scripts/bundle-build/components), then default to a noop version implemented in [scripts/bundle-build/standard-gradle-build/install.sh](scripts/bundle-build/standard-gradle-build/install.sh).
