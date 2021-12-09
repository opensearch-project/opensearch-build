/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */

package jenkins

class Messages implements Serializable {
    def steps

    Messages(steps) {
        this.steps = steps
    }

    // Add a message to the Jenkins queue.
    def add(String stage, String message) {
        this.steps.writeFile(file: "messages/${stage}.msg", text: message)
        this.steps.stash(includes: "messages/*" , name: "messages-${stage}")
    }

    // Load all message in the jenkins queue and append them with a leading newline into a mutli-line string.
    String get(ArrayList stages) {
        // Stages must be explicitly added to prevent overwriting
        // see https://ryan.himmelwright.net/post/jenkins-parallel-stashing/
        
        for (stage in stages) {
            try {
                this.steps.unstash(name: "messages-${stage}")
            } catch(Exception e) {
                echo "No messages found for ${stage}"
            }
        }

        def files = this.steps.findFiles(excludes: '', glob: 'messages/*')
        def data = ""
        for (file in files) {
            data = data + "\n" + this.steps.readFile(file: file.path)
        }

        this.steps.dir('messages') {
            this.steps.deleteDir()
        }

        return data
    }
}