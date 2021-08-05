###Component Build.sh

- Each component should have a corresponding ./build.sh script that is used to prepare their bundle artifacts for a particular
 bundle version.

- OpenSearch core repo will always be built first followed by common-utils. These dependencies will be made available via maven local so
 projects can build against the bleeding edge of these repositories.
 
- A component may depend on a different released version of OpenSearch for a particular build by creating/updating their corresponding
 build.sh and setting the version passed to ./gradlew.
 
- To publish Maven artifacts to central that correlate to a build, place the full path to your maven publications inside
 <component-name>-artifacts/maven. <br>
  Example: OpenSearch-artifacts/maven/org/opensearch/common-utils/1.0.0.0
  <br>
  These will be published as part of a separate release workflow to a staging maven repo.  If this bundle
  build is released, the corresponding maven publications will be promoted to central.
 
Usage: 
- Inputs: build.sh -opensearch_version -architecture(x86/arm64)
- Expected Outputs - a folder at <component-name>-artifacts containing all artifacts that should be included in the bundle