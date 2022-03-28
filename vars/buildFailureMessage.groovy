import com.cloudbees.groovy.cps.NonCPS
import org.apache.commons.io.IOUtils
@NonCPS
def call(){
    String ERROR_STRING = "ERROR"
    List<String> message = []
    Reader performance_log = currentBuild.getRawBuild().getLogReader()
    String logContent = IOUtils.toString(performance_log)
    performance_log.close()
    performance_log = null
    logContent.eachLine() { line ->
        if (line.matches(".*?$ERROR_STRING(.*?)")) {
            line=line.replace("\"", "")
            message.add(line)
        }
    }
    if(message.isEmpty()){
        message=["Build failed"]
    }
    return message
}