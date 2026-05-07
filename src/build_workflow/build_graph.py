# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import threading
from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Callable, Dict, List, Optional, Set


class BuildGraph:
    """
    Manages a dependency graph of build components and executes them
    in parallel respecting dependency ordering.
    """

    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.dependents: Dict[str, Set[str]] = defaultdict(set)
        self.components: List[str] = []

    def add_component(self, name: str, depends_on: Optional[List[str]] = None) -> None:
        self.components.append(name)
        if depends_on:
            for dep in depends_on:
                if dep in self.components:
                    self.dependencies[name].add(dep)
                    self.dependents[dep].add(name)

    def execute_parallel(
        self,
        build_fn: Callable[[str], None],
        required_components: List[str],
        continue_on_error: bool = False,
    ) -> List[str]:
        """
        Execute builds in parallel respecting dependencies.
        All components are submitted immediately but each waits for its
        dependencies to complete before starting its build.

        Returns a list of failed component names.
        """
        failed: List[str] = []
        lock = threading.Lock()
        completed_event: Dict[str, threading.Event] = {name: threading.Event() for name in self.components}

        def wait_for_deps(name: str) -> bool:
            for dep in self.dependencies[name]:
                completed_event[dep].wait()
                with lock:
                    if dep in failed:
                        return False
            return True

        def run_component(name: str) -> str:
            if not wait_for_deps(name):
                with lock:
                    failed.append(name)
                    completed_event[name].set()
                logging.info(f"Skipping {name} because a dependency failed.")
                return name

            try:
                build_fn(name)
                completed_event[name].set()
                return ""
            except Exception:
                with lock:
                    failed.append(name)
                    completed_event[name].set()
                if not continue_on_error or name in required_components:
                    raise
                return name

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures: Dict[Future, str] = {}

            for name in self.components:
                future = executor.submit(run_component, name)
                futures[future] = name

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    executor.shutdown(wait=False, cancel_futures=True)
                    raise

        return failed
