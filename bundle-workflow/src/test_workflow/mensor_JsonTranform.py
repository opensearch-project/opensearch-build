# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import json

import json2table


class JsonTransformation:

    def convert_to_html(self, json_file, path_to_jsonfile):
        with open(path_to_jsonfile + '/' + json_file) as file:
            try:
                infoFromJson = json.load(file)
                testExecutionId = infoFromJson['testExecutionId']
                build_direction = "TOP_TO_BOTTOM"
                table_attributes = {"style": "width:100%", "border": "solid"}
                stored = json2table.convert(infoFromJson,
                                            build_direction=build_direction,
                                            table_attributes=table_attributes)
                return stored, "successful", testExecutionId
            except:
                return json_file, "error", None
