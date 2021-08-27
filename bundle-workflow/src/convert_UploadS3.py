# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#!/usr/bin/env python3

import json
import boto3
import read_write_s3
import os
import sys
import argparse


class convertWrite:
    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-op", "--opfile", help="Result file")
        parser.add_argument("-r", "--assume", help="Assume role")
        parser.add_argument("-s", "--session", help="Session name")
        parser.add_argument("-b", "--bktname", help="Bucketname")
        parser.add_argument("-ob", "--objpath", help="ObjectPath in Bucket")
        parser.add_argument("-fp", "--filepath", help="Filepath of the result file")

        args = parser.parse_args()

        return args

    def conversion_HTML(self, args):
        with open(args.filepath + args.opfile) as json_data:
            try:
                data = json.load(json_data)
                testExecutionId = data['testExecutionId']
                filename = "%s.html" % testExecutionId
                values = {1: 'opCount', 2: 'opErrorCount', 3: 'opErrorRate', 4: 'p0', 5: 'p50', 6: 'p100', 7: 'p50',
                          8: 'p90',
                          9: 'p99', 10: 'p100'}

                stored = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10'}

                testParameters = {1: 'testExecutionId', 2: 'testOwner', 3: 'testStartTime', 4: 'testEndTime',
                                  5: 'testDuration'}

                sut_Parameters = {1: 'dataNodeCount', 2: 'masterNodeCount', 3: 'dataNodeInstanceType',
                                  4: 'masterNodeInstanceType', 5: 'elasticsearchDistributionType', 6: 'aes',
                                  7: 'clusterName', 8: 'awsAccount', 9: 'endpoint',
                                  10: 'region'}
                work_config = {1: 'dataset', 2: 'warmupIterations', 3: 'testIterations'}

                def testResults_OS(arg1):
                    if arg1 == 'index':
                        arg1 = 'index'
                    else:
                        arg1 = 'query'

                    for i in range(1, 11):
                        if i == 4 or i == 5 or i == 6:
                            val = data['testResults']['operationsSummary'][arg1]['requestsPerSecond'][values[i]]
                            stored[i] = val
                            print(stored[i])
                        elif i == 7 or i == 8 or i == 9 or i == 10:
                            val = data['testResults']['operationsSummary'][arg1]['latencyMillis'][values[i]]
                            stored[i] = val
                            print(stored[i])
                        else:
                            val = data['testResults']['operationsSummary'][arg1][values[i]]
                            stored[i] = val
                            print(stored[i])
                    return stored

                def testResults_Operations(arg1):
                    if arg1 == 'auto-date-histogram':
                        arg1 = 'auto-date-histogram'
                    elif arg1 == 'date-histogram-with-tz':
                        arg1 = 'date-histogram-with-tz'
                    elif arg1 == 'date-histogram':
                        arg1 = 'date-histogram'
                    elif arg1 == 'auto-date-histogram-with-tz':
                        arg1 = 'auto-date-histogram-with-tz'
                    else:
                        arg1 = 'index-append'

                    for i in range(1, 11):
                        if i == 4 or i == 5 or i == 6:
                            val = data['testResults']['operations'][arg1]['requestsPerSecond'][values[i]]
                            stored[i] = val
                            print(stored[i])
                        elif i == 7 or i == 8 or i == 9 or i == 10:
                            val = data['testResults']['operations'][arg1]['latencyMillis'][values[i]]
                            stored[i] = val
                            print(stored[i])
                        else:
                            val = data['testResults']['operations'][arg1][values[i]]
                            stored[i] = val
                            print(stored[i])
                    return stored

                def testResults_Stats(arg1):
                    if arg1 == 'cpuStats':
                        arg1 = 'cpuStats'
                    else:
                        arg1 = 'memoryStats'

                    for i in range(7, 11):
                        val = data['testResults'][arg1]['overall'][values[i]]
                        stored[i] = val
                        print(stored[i])
                    return stored

                def testResults_Garbage():
                    place_holder = {1: '1', 2: '2'}
                    old = data['testResults']['garbageCollection']['overall']['oldGCTimeMillis']
                    new = data['testResults']['garbageCollection']['overall']['youngGCTimeMillis']
                    place_holder[1] = old
                    place_holder[2] = new
                    print(stored[i])
                    return stored

                text = """
                            <html>
                            <body>
                            <h1 style="margin-left: auto; margin-right: auto;">Test Result Reports</h1>
                            <h2>Test Details</h2>
                            <table border="2" style="margin-left: auto; margin-right: auto;">
                            <tr>
                                <th>testExecutionId</th>
                                <th>testOwner</th> 
                                <th>testStartTime</th> 
                                <th>testEndTime</th> 
                                <th>testDuration</th> 
                            </tr>
                            <tr>      
                """
                for i in range(1, 6):
                    if (i < 3):
                        text = text + "<td>" + str(data[testParameters[i]]) + "</td>"
                    else:
                        text = text + "<td>" + str(data['testResults'][testParameters[i]]) + "</td>"
                text = text + "</tr>" + \
                       """
                                       </table>
                                       <h2>operationsSummary</h2>
                                       <table border="2" style="margin-left: auto; margin-right: auto;">
                                       <col>
                                       <colgroup span="2"></colgroup>
                                       <colgroup span="2"></colgroup>
                                       <tr>
                                        <td rowspan="2"></td>
                                        <th colspan="3" scope="colgroup">operationsCount</th>
                                        <th colspan="3" scope="colgroup">requestsPerSecond</th>
                                        <th colspan="4" scope="colgroup">latencyMillis</th>
                                       </tr>
                                       <tr>
                                           <th scope="col">opCount</th>
                                           <th scope="col">opErrorCount</th>
                                           <th scope="col">opErrorRate</th>
                                           <th scope="col">p0</th>
                                           <th scope="col">p50</th>
                                           <th scope="col">p100</th>
                                           <th scope="col">p50</th>
                                           <th scope="col">p90</th>
                                           <th scope="col">p99</th>
                                           <th scope="col">p100</th>
                                       </tr>
                                       <tr>
                                         <th scope="row">index</th>
                       """
                it = testResults_OS('index')
                for i in range(1, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """        
                                       <tr>
                                        <th scope="row">query</th>
                       """
                it = testResults_OS('query')
                for i in range(1, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """    
                                   </table>
       
                                   <h2>operations</h2>
                                   <table border="2" style="margin-left: auto; margin-right: auto;">
                                   <col>
                                   <colgroup span="2"></colgroup>
                                   <colgroup span="2"></colgroup>
                                   <tr>
                                   <td rowspan="2"></td>
                                   <th colspan="3" scope="colgroup">operationsCount</th>
                                   <th colspan="3" scope="colgroup">requestsPerSecond</th>
                                   <th colspan="4" scope="colgroup">latencyMillis</th>
                                   </tr>
                                   <tr>
                                    <th scope="col">opCount</th>
                                    <th scope="col">opErrorCount</th>
                                    <th scope="col">opErrorRate</th>
                                    <th scope="col">p0</th>
                                    <th scope="col">p50</th>
                                    <th scope="col">p100</th>
                                    <th scope="col">p50</th>
                                    <th scope="col">p90</th>
                                    <th scope="col">p99</th>
                                    <th scope="col">p100</th>
                                   </tr>
                                   <tr>
                                       <th scope="row">auto-date-histogram</th>
                       """
                it = testResults_Operations('auto-date-histogram')
                for i in range(1, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """
                                   <tr>
                                       <th scope="row">date-histogram-with-tz</th>
                       """
                it = testResults_Operations('date-histogram-with-tz')
                for i in range(1, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """
                                   <tr>
                                       <th scope="row">date-histogram</th>
                       """
                it = testResults_Operations('date-histogram')
                for i in range(1, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """
                                    <tr>
                                       <th scope="row">auto-date-histogram-with-tz</th>
                       """
                it = testResults_Operations('auto-date-histogram-with-tz')
                for i in range(1, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """
                                   <tr>
                                       <th scope="row">index-append</th>
                       """
                it = testResults_Operations('index-append')
                for i in range(1, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """
                                   </table>
                                   <h3>cpuStats and memoryStats</h3>    
                                   <table border="2" style="margin-left: auto; margin-right: auto;">
                                     <col>
                                     <colgroup span="2"></colgroup>
                                     <colgroup span="2"></colgroup>
                                     <tr>
                                       <td rowspan="2"></td>
                                       <th colspan="4" scope="colgroup">overall</th>
                                     </tr>
                                     <tr>
                                       <th scope="col">p50</th>
                                       <th scope="col">p90</th>
                                       <th scope="col">p99</th>
                                       <th scope="col">p100</th>
                                     </tr>
                                     <th scope="row">cpuStats</th>
                       """
                it = testResults_Stats('cpuStats')
                for i in range(7, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """
                                   <th scope="row">memoryStats</th>
                       """
                it = testResults_Stats('memoryStats')
                for i in range(7, 11):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """
                                </table>
                               <h2>garbageCollection</h2>
                               <h4>overall</h4>
                               <table border="2" style="margin-left: auto; margin-right: auto;">
                                   <tr>
                                       <th>oldGCTimeMillis</th>
                                       <th>youngGCTimeMillis</th> 
                                   </tr>
                                   <tr>
                       """
                it = testResults_Garbage()
                for i in range(1, 3):
                    text = text + "<td>" + str(it.get(i)) + "</td>"
                text = text + "</tr>" + \
                       """
                                   </table>
                                   <h2>SystemUnderTest</h2>
                                   <table border="2" style="margin-left: auto; margin-right: auto;">
                                   <tr>
                                       <th>dataNodeCount</th>
                                       <th>masterNodeCount</th> 
                                       <th>dataNodeInstanceType</th> 
                                       <th>masterNodeInstanceType</th> 
                                       <th>elasticsearchDistributionType</th> 
                                       <th>aes</th> 
                                       <th>clusterName</th> 
                                       <th>awsAccount</th> 
                                       <th>endpoint</th> 
                                       <th>region</th> 
                                   </tr>
                                   <tr>
                       """
                for i in range(1, 11):
                    if (i < 7):
                        text = text + "<td>" + str(data['systemUnderTest'][sut_Parameters[i]]) + "</td>"
                    else:
                        text = text + "<td>" + str(
                            data['systemUnderTest']['clusterIdentity'][sut_Parameters[i]]) + "</td>"
                text = text + "</tr>" + \
                       """
                                   </table>
                                   <h2>Workload Config</h2>
                                   <table border="2" style="margin-left: auto; margin-right: auto;">
                                   <tr>
                                       <th>dataset</th>
                                       <th>warmupIterations</th> 
                                       <th>testIterations</th>
                                   </tr>
                                   <tr>
                       """
                for i in range(1, 4):
                    text = text + "<td>" + str(data['workloadConfig'][work_config[i]]) + "</td>"
                text = text + "</tr>" + \
                       """
                                   </table>
                                   </body>
                                   </html>
       
                       """.format(**locals())
                file1 = open(filename, 'w')
                file1.write(text)
                file1.close()
                objectname = read_write_s3.read_write_files(args.assume, args.session)
                objectname.put_S3Objects(args.bktname, filename, args.objpath + filename)
                os.remove("%s" % args.opfile)
                os.remove("%s" % filename)
            except:
                txt_file = open(args.opfile, "r")
                data = txt_file.read()
                file1 = open("error_sample.html", "w")
                file1.write(data)
                file1.close()
                objectname = read_write_s3.read_write_files(args.assume, args.session)
                objectname.put_S3Objects(args.bktname, "error_sample.html", args.objpath + "error_sample.html")
                os.remove("%s" % args.opfile)
                os.remove("error_sample.html")


convert_write = convertWrite()
args = convert_write.parse_arguments()
convert_write.conversion_HTML(args)