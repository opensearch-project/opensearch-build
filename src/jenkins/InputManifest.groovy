/*
 * Copyright OpenSearch Contributors
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
        String qualifier
        String platform
        String architecture

        Build(Map data) {
            this.name = data.name
            this.version = data.version
            this.qualifier = data.qualifier
            this.platform = data.platform
            this.architecture = data.architecture
        }

        String getFilename() {
            return this.name.toLowerCase().replaceAll(' ', '-')
        }
    }

    Build build
    Ci ci

    InputManifest(Map data) {
        this.build = new InputManifest.Build(data.build)
        this.ci = data.ci ? new InputManifest.Ci(data.ci) : null
    }

    String getSHAsRoot(String jobName) {
        return [
            jobName,
            this.build.version,
            'shas'
        ].join("/")
    }
}
