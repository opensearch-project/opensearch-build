# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse


class CompareArgs:
    id1: str
    id2: str
    results_format: str
    results_numbers_align: str
    results_file: str
    show_in_results: str

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="Compare two IDs")
        self.parser.add_argument("id1", type=str, help="The baseline ID to compare")
        self.parser.add_argument("id2", type=str, help="The contender ID to compare")
        self.parser.add_argument("--results-format", type=str, help="Defines the output format for the results, markdown or csv (default: markdown)")
        self.parser.add_argument("--results-numbers-align", type=str, help="Defines the format for the command line results. (Default: right)")
        self.parser.add_argument("--results-file", type=str, help="File path to write the results file to")
        self.parser.add_argument("--show-in-results", type=str, help="Determines whether to include the comparison in the results file")
        self.args = self.parser.parse_args()

        self.id1 = self.args.id1
        self.id2 = self.args.id2
        self.results_format = self.args.results_format if self.args.results_format else "markdown"
        self.results_numbers_align = self.args.results_numbers_align if self.args.results_numbers_align else "right"
        self.results_file = self.args.results_file if self.args.results_file else None
        self.show_in_results = self.args.show_in_results if self.args.show_in_results else None


if __name__ == "__main__":
    try:
        compare_args = CompareArgs()
    except argparse.ArgumentError as e:
        print(f"Error: {e}")
