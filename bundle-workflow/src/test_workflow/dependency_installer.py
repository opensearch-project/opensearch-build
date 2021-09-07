import os
import shutil

from aws.s3_bucket import S3Bucket


class DependencyInstaller:
    """
    Provides a dependency installer for the test suites.
    """

    def __init__(self, build):
        self.build_id = build.id
        self.version = build.version
        self.arch = build.architecture
        self.s3_maven_location = (
            f"/builds/{self.version}/{self.build_id}/{self.arch}/maven/org/opensearch"
        )
        self.s3_build_location = (
            f"/builds/{self.version}/{self.build_id}/{self.arch}/plugins"
        )

    def install_maven_dependencies(self, dependency_dict):
        """
        Downloads the maven dependencies from S3 and puts them on the maven local path
        for each dependency in the dependency_list.

        :param dependency_dict: list of dependency names with version for which the maven artifacts need to be downloaded.
        Example: {'opensearch-job-scheduler':'1.1.0.0', 'opensearch-core':'1.1.0'}
        """
        s3_bucket = S3Bucket(self.s3_maven_location)
        for dependency, version in dependency_dict.items():
            s3_path = f"{dependency}/{version}"
            maven_local_path = os.path.join(
                os.path.expanduser("~"),
                f".m2/repository/org/opensearch/{dependency}/{version}/",
            )
            s3_bucket.download_folder(s3_path, maven_local_path)

    def install_build_dependencies(self, dependency_dict, custom_local_path):
        """
        Downloads the build dependencies from S3 and puts them on the given custom path
        for each dependency in the dependency_list.

        :param dependency_list: list of dependency names with version for which the build artifacts need to be downloaded.
        Example: {'opensearch-job-scheduler':'1.1.0.0'}
        :param custom_local_path: the path where the downloaded dependencies need to copied.
        """
        s3_bucket = S3Bucket(self.s3_build_location)
        for dependency, version in dependency_dict.items():
            s3_path = f"{dependency}-{version}.zip"
            s3_bucket.download_file(s3_path, custom_local_path)

    def cleanup(self, local_path):
        """
        Provides functionality to clean up the downloaded contents in a maven local path or a custom path.
        """
        try:
            if os.path.isfile(local_path) or os.path.islink(local_path):
                os.unlink(local_path)
            elif os.path.isdir(local_path):
                shutil.rmtree(local_path)
        except OSError as e:
            print(f"Failed to clean {local_path}. Reason: {e}")
            raise
