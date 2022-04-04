import com.cloudbees.groovy.cps.NonCPS
import org.apache.commons.io.IOUtils
@NonCPS
def call(){
    String ERROR_STRING = "Error"
    List<String> message = []
    Reader performance_log = currentBuild.getRawBuild().getLogReader()
    String logContent = IOUtils.toString(performance_log)
    performance_log.close()
    performance_log = null
    logContent.eachLine() { line ->
        line=line.replace("\"", "")
        def match = (line =~ /$ERROR_STRING.*/) 
        if (match.find()) {
            line=match[0]
            message.add(line)
        }
        //if (line.matches(".*?$ERROR_STRING(.*?)")) {
        //    line=line.replace("\"", "")
        //    def matches = (articleContent =~ /$ERROR_STRING.*/) 
        //    def firstmatch = matches[0]
        //    message.add(firstmatch)
        //}
    }
    if(message.isEmpty()){
        message=["Build failed"]
    }
    return message
}