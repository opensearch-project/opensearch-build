# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import sys

from system import console
from system.temporary_directory import TemporaryDirectory
from validation_workflow.validation_args import ValidationArgs
from validation_workflow.validation_test_runner import ValidationTestRunner  # type: ignore


def main() -> int:
    args = ValidationArgs()

    console.configure(level=args.logging_level)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    if args.skip_core_plugins is None:
        logging.info("Native plugin validation: installing all plugins")
    elif args.skip_core_plugins:
        logging.info(f"Native plugin validation: skipping specific plugins: {args.skip_core_plugins}")
    else:
        logging.info("Native plugin validation: skipping all plugins")

    with TemporaryDirectory() as work_dir:
        if args.distribution == "docker":
            docker_source = args.docker_source
            for source in docker_source:
                docker_args = args
                docker_args.docker_source = source
                test_result = ValidationTestRunner.dispatch(docker_args, args.distribution, work_dir).run()

        else:
            test_result = ValidationTestRunner.dispatch(args, args.distribution, work_dir).run()
        logging.info(f'final test_result = {test_result}\n\n')
        return 0 if test_result else 1  # type: ignore


if __name__ == "__main__":
    sys.exit(main())
