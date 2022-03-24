@NonCPS
def call(){
    def String ERROR_STRING = "ERROR"
    def String message = ""
    def String delimiter = ","
    def performance_log = currentBuild.rawBuild.getLog(Integer.MAX_VALUE).join('\n')
    performance_log.eachLine() { line ->
        if (line.matches(".*$ERROR_STRING.*")) {
            message+=(line+delimiter)
        }
    }
    message=message.replaceAll(",", "\n")
    if(message.isEmpty()){
        message="Build failed"
    }
    return message
}
