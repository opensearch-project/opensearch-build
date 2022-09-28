/*
 * Copyright OpenSearch Contributors
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins

class TestManifest {
    class Ci implements Serializable {
        class Image implements Serializable {
            String name
            String args

            Image(Map data) {
                this.name = data.name
                this.args = data.args
            }
        }

        Image image

        Ci(Map data) {
            this.image = new TestManifest.Ci.Image(data.image)
        }
    }

    String name

    Ci ci

    TestManifest(Map data) {
        this.name = data.name
        this.ci = data.ci ? new TestManifest.Ci(data.ci) : null
    }
}
