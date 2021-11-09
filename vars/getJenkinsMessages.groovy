/** Load all message in the jenkins queue and append them with a leading newline into a mutli-line string */
String call(ArrayList stages) {
    // Stages must be explicitly added to prevent overwriting
    // See https://ryan.himmelwright.net/post/jenkins-parallel-stashing/
    for (stage in stages) {
        unstash "notifications-${stage}"
    }

    def files = findFiles(excludes: '', glob: 'notifications/*')
    def data = ""
    for (file in files) {
        data = data + "\n" + readFile (file: file.path)
    }

    // Delete all the notifications from the workspace
    dir('notifications') {
        deleteDir()
    }
    return data
}
