/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */


package jenkins


class BundleManifest implements Serializable {
    class Build implements Serializable {
        String id
        String name
        String version
        String platform
        String architecture
        String distribution
        String location

        Build(Map data) {
            this.id = data.id
            this.name = data.name
            this.version = data.version
            this.platform = data.platform
            this.architecture = data.architecture
            this.distribution = data.distribution
            this.location = data.location
        }

        String getFilename() {
            return this.name.toLowerCase().replaceAll(' ', '-')
        }

        String getBuildLocation() {
            return this.location
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
        String location

        Component(Map data) {
            this.name = data.name
            this.version = data.version
            this.ref = data.ref
            this.commit_id = data.commit_id
            this.repository = data.repository
            this.location = data.location
        }

    }

    Build build
    Components components

    BundleManifest(Map data) {
        this.build = new BundleManifest.Build(data.build)
        this.components = new BundleManifest.Components(data.components)
    }

    public String getArtifactArchitecture() {
        return this.build.architecture
    }

    public String getArtifactBuildId() {
        return this.build.id
    }

    public String getDistribution() {
        return this.build.distribution
    }

    public String getCommitId (String name) {
        return this.components.get(name).commit_id
    }

    public ArrayList getNames() {
        def componentsName = []
        this.components.each{key, value -> componentsName.add(key)}
        return componentsName
    }

    public String getRepo(String name) {
        return this.components.get(name).repository
    }

    public String getLocation(String name) {
        return this.components.get(name).location
    }
}
