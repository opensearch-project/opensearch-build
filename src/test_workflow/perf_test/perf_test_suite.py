import os
import subprocess


class PerfTestSuite:
    """
    Represents a performance test suite. This class runs rally test on the deployed cluster with the provided IP.
    """
    def __init__(self, bundle_manifest, endpoint, security, current_workspace, test_results_path, args):
        self.manifest = bundle_manifest
        self.work_dir = "mensor/"
        self.endpoint = endpoint
        self.security = security
        self.current_workspace = current_workspace
        self.args = args
        self.command = (
            f"pipenv run python test_config.py -i {self.endpoint} -b {self.manifest.build.id}"
            f" -a {self.manifest.build.architecture} -p {self.current_workspace}"
            f" --workload {self.args.workload} --workload-options '{self.args.workload_options}'"
            f" --warmup-iters {self.args.warmup_iters} --test-iters {self.args.test_iters}"
        )

        if test_results_path is not None:
            self.command = (
                f"pipenv run python test_config.py -i {self.endpoint} -b {self.manifest.build.id}"
                f" -a {self.manifest.build.architecture} -p {test_results_path}"
            )

        print(self.command)

    def execute(self):
        try:
            os.chdir(os.path.join(self.current_workspace, self.work_dir))
            dir = os.getcwd()
            subprocess.check_call("python3 -m pipenv install", cwd=dir, shell=True)
            subprocess.check_call("pipenv install", cwd=dir, shell=True)

            if self.security:
                subprocess.check_call(f"{self.command} -s", cwd=dir, shell=True)
            else:
                subprocess.check_call(f"{self.command}", cwd=dir, shell=True)
        finally:
            os.chdir(self.current_workspace)
