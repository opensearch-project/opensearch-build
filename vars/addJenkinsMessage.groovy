/** Add a message to the jenkins queue */
def call(String stage, String message) {
    writeFile(file: "notifications/${stage}.msg", text: message)
    stash(includes: "notifications/*" , name: "notifications-${stage}")
}
