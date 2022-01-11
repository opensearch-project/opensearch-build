- [Assemble a Distribution](#assemble-a-distribution)
  - [Assemble.sh Options](#assemblesh-options)
  - [Custom Install Scripts](#custom-install-scripts)

## Assemble a Distribution 

```bash
./assemble.sh builds/opensearch/manifest.yml
```

```bash
./assemble.sh builds/opensearch/manifest.yml --distribution rpm
```

The assembling step takes output from the build step, installs plugins, and assembles a full distribition into the `dist` folder. The input requires a path to the build manifest and is expected to be inside the `builds` directory that contains `dist`, `maven`, `plugins` and `core-plugins` subdirectories from the build step.

Artifacts will be created as follows.

```
/dist
  <file-name>.tar.gz or .zip or .rpm <- assembled tar or zip or rpm depending on the value of `--distribution`, default to `tar'
  manifest.yml <- bundle manifest describing versions for the min bundle and all installed plugins and their locations
```

### Assemble.sh Options

The following options are available in `assemble.sh`.

| name               | description                                                                                       |
|--------------------|---------------------------------------------------------------------------------------------------|
| -b, --base-url     | The base url to download the artifacts.                                                           |
| -d, --distribution | Specify what distribution to bundle, default to 'tar'. <br> Options include tar/zip/rpm.          |
| --keep             | Do not delete the temporary working directory on both success or error.                           |
| -v, --verbose      | Show more verbose output.                                                                         |

### Custom Install Scripts

You can perform additional plugin install steps by adding an `install.sh` script. By default the tool will look for a script in [scripts/bundle-build/components](../../scripts/bundle-build/components), then default to a noop version implemented in [scripts/default/install.sh](../../scripts/default/install.sh).

### Assemble RPM package

Assemble workflow utilizes [FPM](https://fpm.readthedocs.io/en/latest/) internally to build RPM package based on the tar.gz/zip generated from build_workflow.

These are the requirements for generating an RPM package correctly:
* We only support generating RPM for RedHat based LINUX distros in our [compatibility page](https://opensearch.org/docs/opensearch/install/compatibility/)
* You need to run the assemble workflow on a LINUX machine with ruby-2.3.0+ and fpm 1.12.0+ installed, as well as these [dependency pacakges](https://fpm.readthedocs.io/en/latest/installation.html#installing-optional-dependencies)
* We currently do not support building RPM on macOS or BSD, due to limitations on FPM utility
* We have published the design of assembling RPM package, please check this [issue post](https://github.com/opensearch-project/opensearch-build/issues/1452) for more information
