@NonCPS
import java.io.Reader;
def call(){
    def String ERROR_STRING = "ERROR"
    def String message = ""
    def String delimiter = ","
    Reader performance_log = currentBuild.getRawBuild().getLogReader().join('\n')
    String logContent = IOUtils.toString(performance_log)
    performance_log.close();
    performance_log = null
    logContent.eachLine() { line ->
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
