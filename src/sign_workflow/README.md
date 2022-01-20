- [Signing Artifacts](#signing-artifacts)
  - [Sign.sh Options](#signsh-options)

## Signing Artifacts

The signing step (optional) takes the manifest file created from the build step and signs all its component artifacts using a tool called `opensearch-signer-client` (in progress of being open-sourced). The input requires a path to the build manifest and is expected to be inside the artifacts directory with the same directories mentioned in the build step. 

```bash
./sign.sh builds/opensearch/manifest.yml
```

### Sign.sh Options

The following options are available. 

| name          | description                                                                                  |
| ------------- | -------------------------------------------------------------------------------------------- |
| target        | Path to local manifest file or artifact directory.                                           |
| --component   | The name of the component whose artifacts will be signed, if using a manifest target.        |
| --type        | The artifact type to be signed, if using a manifest target, can be [plugins, maven, bundle]. |
| --sigtype     | Type of Signature file, can be [.asc, .sig].                                                 |
| -v, --verbose | Show more verbose output.                                                                    |

The signed artifacts (<artifact>.asc) will be found in the same location as the original artifact. 
