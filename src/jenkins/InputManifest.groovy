/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins

class InputManifest {
    class Ci implements Serializable {
        class Image implements Serializable {
            String name
            String args

            Image(Map data) {
                this.name = data.name

                if (this.name == null) {
                    error("Missing ci.image.name")
                }

                this.args = data.args
            }
        }

        Image image

        Ci(Map data) {
            this.image = new InputManifest.Ci.Image(data.image)
        }
    }

    class Build implements Serializable {
        String name
        String version
        String platform
        String architecture

        Build(Map data) {
            this.name = data.name
            this.version = data.version
            this.platform = data.platform
            this.architecture = data.architecture
        }
    }

    Build build
    Ci ci

    InputManifest(Map data) {
        this.build = new InputManifest.Build(data.build)
        this.ci = new InputManifest.Ci(data.ci)
    }

    public String getPublicDistUrl(String publicArtifactUrl = 'https://ci.opensearch.org/ci/dbc', String jobName, String buildNumber, String platform = null, String architecture = null) {
        return [
            publicArtifactUrl,
            jobName,
            this.build.version,
            buildNumber,
            platform ?: this.build.platform,
            architecture ?: this.build.architecture,
            'dist',
            "${this.build.name.toLowerCase().replaceAll(' ', '-')}-${this.build.version}-${platform}-${architecture}.${platform == 'windows' ? 'zip' : 'tar.gz'}"
        ].join("/")
    }

    public String getSHAsRoot(String jobName, String platform = null, String architecture = null) {
        return [
            jobName,
            'shas',
            this.build.version,
            platform ?: this.build.platform,
            architecture ?: this.build.architecture
        ].join("/")
    }
}
