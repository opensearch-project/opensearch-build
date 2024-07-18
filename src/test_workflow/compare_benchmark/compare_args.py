# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import re

class ValidateID(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        if not re.match(r'^[a-zA-Z0-9-]+$', values):
            parser.error(f"Invalid ID: {values}")
        setattr(args, self.dest, values)

class CompareArgs:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Compare two IDs")
        self.parser.add_argument("id1", type=str, help="The baseline ID to compare", action=ValidateID)
        self.parser.add_argument("id2", type=str, help="The contender ID to compare", action=ValidateID)
        self.parser.add_argument("--results-format", type=str, help="Defines the output format for the results, markdown or csv (default: markdown)")
        self.parser.add_argument("--results-numbers-align", type=str, help="Defines the format for the command line results. (Default: right)")
        self.parser.add_argument("--results-file", type=str, help="File path to write the results file to")
        self.parser.add_argument("--show-in-results", type=str, help="Determines whether to include the comparison in the results file")
        self.args = self.parser.parse_args()

    @property
    def id1(self):
        return self.args.id1

    @property
    def id2(self):
        return self.args.id2
    
    @property
    def results_format(self):
        return self.args.results_format
    
    @property
    def results_numbers_align(self):
        return self.args.results_numbers_align
    
    @property
    def results_file(self):
        return self.args.results_file
    
    @property
    def show_in_results(self):
        return self.args.show_in_results

if __name__ == "__main__":
    try:
        compare_args = CompareArgs()
    except argparse.ArgumentError as e:
        print(f"Error: {e}")