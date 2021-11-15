/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins

import groovy.transform.InheritConstructors

@InheritConstructors
class InputManifest extends Manifest {
    class Ci implements Serializable {
        Map data

        String dockerImage
        String dockerArgs

        Ci(Map data) {
            this.data = data
        }

        public String getDockerImage() {
            def val = this.data?.image?.name

            if (val == null) {
                error("Missing ci.image.name in ${this.filename}")
            }

            return val
        }

        public String getDockerArgs() {
            return this.data?.image?.args
        }
    }

    Ci ci

    def getCi() {
        return new InputManifest.Ci(this.data.ci)
    }
}


