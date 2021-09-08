import os

from aws.s3_bucket import S3Bucket


class DependencyInstaller:
    """
    Provides a dependency installer for the test suites.
    """

    ARTIFACT_S3_BUCKET = "artifact-bucket-stack-buildbucket-9omh0hnpg12q"

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
        s3_bucket = S3Bucket(self.ARTIFACT_S3_BUCKET)
        for dependency, version in dependency_dict.items():
            s3_path = f"{self.s3_maven_location}/{dependency}/{version}"
            maven_local_path = self.maven_local_path(dependency, version)
            s3_bucket.download_folder(s3_path, maven_local_path)

    def install_build_dependencies(self, dependency_dict, custom_local_path):
        """
        Downloads the build dependencies from S3 and puts them on the given custom path
        for each dependency in the dependency_list.

        :param dependency_list: list of dependency names with version for which the build artifacts need to be downloaded.
        Example: {'opensearch-job-scheduler':'1.1.0.0'}
        :param custom_local_path: the path where the downloaded dependencies need to copied.
        """
        s3_bucket = S3Bucket(self.ARTIFACT_S3_BUCKET)
        for dependency, version in dependency_dict.items():
            s3_path = f"{self.s3_build_location}/{dependency}-{version}.zip"
            s3_bucket.download_file(s3_path, custom_local_path)

    def maven_local_path(self, dependency, version):
        return os.path.join(
            os.path.expanduser("~"),
            f".m2/repository/org/opensearch/{dependency}/{version}/",
        )
