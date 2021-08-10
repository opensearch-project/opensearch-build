## Bundle Build

Builds the OpenSearch bundle.

The OpenSearch repo is built first, followed by common-utils. These dependencies are published to maven local, and subsequent project builds pick up those. All final output is placed into an `artifacts` folder along with a `manifest.yml` that contains output details.

### Usage

```bash
./bundle-workflow/build.sh manifests/opensearch-1.0.0.yml
```

### Scripts

Each component build relies on a `build.sh` script that is used to prepare bundle artifacts for a particular bundle version that takes two arguments: version and target architecture. By default the tool will look for a script in [scripts/bundle-build/components](../../scripts/bundle-build/components), then in the checked-out repository in `build/build.sh`, then default to a Gradle build implemented in [scripts/bundle-build/standard-gradle-build](../../scripts/bundle-build/standard-gradle-build).