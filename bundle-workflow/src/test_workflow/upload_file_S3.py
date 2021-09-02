# !/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import argparse
import json
import os

import JsonTransform

from src import s3_utility


class UploadFile:
    """
    result_file- the file where the console output will be stored
    bucket_name- Name of the Bucket
    object_path- Path in the Bucket where you want to store the file
    file_path- File path where the console output result_file is present
    """

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--result_file", help="Result file", required=True)
        parser.add_argument("-b", "--bucket_name", help="Bucket name", required=True)
        parser.add_argument("-o", "--object_path", help="ObjectPath in Bucket", required=True)
        parser.add_argument("-f", "--file_path", help="Filepath of the result file", required=True)

        args = parser.parse_args()

        return args

    def conversion_to_html(self, args):
        convertobj = test1.Test1()
        html_string, output, id = convertobj.convert_to_html(args.result_file, args.file_path)
        if (output == "successful"):
            filename = "%s.html" % id
            text_file = open(filename, "w")
            text_file.write(html_string)
            text_file.close()
            return filename
        else:
            txt_file = open(html_string, "r")
            data = txt_file.read()
            file1 = open("error.html", "w")
            file1.write(data)
            file1.close()
            return "error.html"

    def put_into_S3(self, args, filename):
        objectname = S3ReadWrite()
        objectname.upload_file(filename, args.bucket_name, args.object_path + '/' + filename)
        objectname.upload_file(args.result_file, args.bucket_name, args.object_path + '/' + args.result_file)
        os.remove("%s" % args.result_file)
        os.remove("%s" % filename)


convert_write = UploadFile()
args = convert_write.parse_arguments()
document = convert_write.conversion_to_html(args)
convert_write.put_into_S3(args, document)