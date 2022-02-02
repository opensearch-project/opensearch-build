/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins

class BuildManifest implements Serializable {
    class Build implements Serializable {
        String id
        String name
        String version
        String platform
        String architecture

        Build(Map data) {
            this.id = data.id
            this.name = data.name
            this.version = data.version
            this.platform = data.platform
            this.architecture = data.architecture
        }

        String getFilename() {
            return this.name.toLowerCase().replaceAll(' ', '-')
        }

        String getFilenameWithExtension(String platform = null, String architecture = null) {
            String resolvedPlatform = platform ?: this.platform
            String resolvedArchitecture = architecture ?: this.architecture
            return "${this.getFilename()}-${this.version}-${resolvedPlatform}-${resolvedArchitecture}.${resolvedPlatform == 'windows' ? 'zip' : 'tar.gz'}"
        }

        String getPackageName() {
            return [
                    this.getFilename(),
                    this.version,
                    this.platform,
                    this.architecture,
            ].join('-') + '.tar.gz'
        }
    }

    class Components extends HashMap<String, Component> {

        Components(ArrayList data) {
            data.each { item ->
                Component component = new Component(item)
                this[component.name] = component
            }
        }
    }

    class Component implements Serializable {
        String name
        String version
        String ref
        String commit_id
        String repository
        Map<String, ArrayList> artifacts

        Component(Map data) {
            this.name = data.name
            this.version = data.version
            this.ref = data.ref
            this.commit_id = data.commit_id
            this.repository = data.repository
            this.artifacts = data.artifacts ? new HashMap<>(data.artifacts) : new HashMap<>()
        }

    }

    Build build
    Components components

    BuildManifest(Map data) {
        this.build = new BuildManifest.Build(data.build)
        this.components = new BuildManifest.Components(data.components)
    }

    public String getArtifactRoot(String jobName, String buildNumber) {
        return [
                jobName,
                this.build.version,
                buildNumber,
                this.build.platform,
                this.build.architecture
        ].join("/")
    }

    public String getArtifactRootUrl(String publicArtifactUrl = 'https://ci.opensearch.org/ci/dbc', String jobName, String buildNumber) {
        return [
                publicArtifactUrl,
                this.getArtifactRoot(jobName, buildNumber)
        ].join('/')
    }

    public String getUrl(String publicArtifactUrl = 'https://ci.opensearch.org/ci/dbc', String jobName, String buildNumber) {
        return [
            this.getArtifactRootUrl(publicArtifactUrl, jobName, buildNumber),
            'builds',
            this.build.getFilename(),
            'manifest.yml'
        ].join("/")
    }

    public String getArtifactUrl(String publicArtifactUrl = 'https://ci.opensearch.org/ci/dbc', String jobName, String buildNumber) {
        return [
            this.getArtifactRootUrl(publicArtifactUrl, jobName, buildNumber),
            'dist',
            this.build.getFilename(),
            this.build.getFilenameWithExtension()
        ].join("/")
    }

    public String getArtifactArchitecture() {
        return this.build.architecture
    }

    public String getArtifactBuildId() {
        return this.build.id
    }

    public String getMinArtifact() {
        components.get(build.name.replace(' ','-'))?.artifacts?.get("dist")?.first()
    }
}
