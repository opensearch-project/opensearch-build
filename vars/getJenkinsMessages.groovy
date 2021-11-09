/** Load all message in the jenkins queue and append them with a leading newline into a mutli-line string */
String call(ArrayList stages) {
    // Stages must be explicitly added to prevent overwriting
    // See https://ryan.himmelwright.net/post/jenkins-parallel-stashing/
    for (stage in stages) {
        unstash "messages-${stage}"
    }

    def files = findFiles(excludes: '', glob: 'messages/*')
    def data = ""
    for (file in files) {
        data = data + "\n" + readFile (file: file.path)
    }

    // Delete all the messages from the workspace
    dir('messages') {
        deleteDir()
    }
    return data
}
