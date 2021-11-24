# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os


def get_folder_name_from_build_name(name):
    return name.lower().replace(" ", "-")


def get_output_dir(parent_folder, build_name):
    return os.path.join(
        os.getcwd(),
        parent_folder,
        get_folder_name_from_build_name(build_name)
    )
