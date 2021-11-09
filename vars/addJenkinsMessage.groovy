/** Add a message to the jenkins queue */
def call(String stage, String message) {
    writeFile(file: "messages/${stage}.msg", text: message)
    stash(includes: "messages/*" , name: "messages-${stage}")
}
