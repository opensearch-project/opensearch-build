/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * The OpenSearch Contributors require contributions made to
 * this file be licensed under the Apache-2.0 license or a
 * compatible open source license.
 */
import com.cloudbees.groovy.cps.NonCPS
import org.apache.commons.io.IOUtils
@NonCPS
def call(){
    String ERROR_STRING = "Error building"
    List<String> message = []
    Reader performance_log = currentBuild.getRawBuild().getLogReader()
    String logContent = IOUtils.toString(performance_log)
    performance_log.close()
    performance_log = null
    logContent.eachLine() { line ->
        line=line.replace("\"", "")
        //Gets the exact match for Error building
        def java.util.regex.Matcher match = (line =~ /$ERROR_STRING.*/)
        if (match.find()) {
            line=match[0]
            message.add(line)
        }
    }
    //if no match returns as Build failed
    if(message.isEmpty()){
        message=["Build failed"]
    }
    return message
}
