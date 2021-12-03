- [Signing Artifacts](#signing-artifacts)
  - [Sign.sh Options](#signsh-options)

## Signing Artifacts

The signing step (optional) takes the manifest file created from the build step and signs all its component artifacts using a tool called `opensearch-signer-client` (in progress of being open-sourced). The input requires a path to the build manifest and is expected to be inside the artifacts directory with the same directories mentioned in the build step. 

```bash
./sign.sh builds/opensearch/manifest.yml
```

### Sign.sh Options

The following options are available. 

| name          | description                                                                           |
|---------------|---------------------------------------------------------------------------------------|
| --component   | The component name of the component whose artifacts will be signed.                   |
| --type        | The artifact type to be signed. Currently one of 3 options: [plugins, maven, bundle]. |
| -v, --verbose | Show more verbose output.                                                             |

The signed artifacts (<artifact>.asc) will be found in the same location as the original artifact. 
