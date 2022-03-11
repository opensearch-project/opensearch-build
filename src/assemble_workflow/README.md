- [Assemble a Distribution](#assemble-a-distribution)
  - [Assemble.sh Options](#assemblesh-options)
  - [Custom Install Scripts](#custom-install-scripts)

## Assemble a Distribution 

```bash
./assemble.sh builds/opensearch/manifest.yml
```

The assembling step takes output from the build step, installs plugins, and assembles a full distribition into the `dist` folder. The input requires a path to the build manifest and is expected to be inside the `builds` directory that contains `dist`, `maven`, `plugins` and `core-plugins` subdirectories from the build step.

Artifacts will be created as follows.

```
/dist
  <file-name>.tar.gz / .zip / .rpm <- assembled tarball / zip / rpm depending on distribution value in builds/opensearch/manifest.yml, default to tarball if 'distribution' key not found
  manifest.yml <- bundle manifest describing versions for the min bundle and all installed plugins and their locations
```

### Assemble.sh Options

The following options are available in `assemble.sh`.

| name               | description                                                             |
|--------------------|-------------------------------------------------------------------------|
| -b, --base-url     | The base url to download the artifacts.                                 |
| --keep             | Do not delete the temporary working directory on both success or error. |
| -v, --verbose      | Show more verbose output.                                               |

### Custom Install Scripts

You can perform additional plugin install steps by adding an `install.sh` script. By default the tool will look for a script in [scripts/bundle-build/components](../../scripts/bundle-build/components), then default to a noop version implemented in [scripts/default/install.sh](../../scripts/default/install.sh).
