import os
import shutil


class DependencyInstaller:
    """
    Provides functionality to copy the maven dependencies from S3 to maven local to be used by tests.
    """

    def __init__(self, build_id, dependency_name, version, arch):
        self.build_id = build_id
        self.dependency_name = dependency_name
        self.version = version
        self.arch = arch

    def get_dependency_path(self):
        return f"org/opensearch/{self.dependency_name}/{self.version}/"

    def get_maven_local_path(self):
        return os.path.join(
            os.path.expanduser("~"), ".m2/repository/", self.get_dependency_path()
        )

    # TODO: This is currently a stubbed function which returns files from the current directory,
    # to be replaced after it is implemented
    def download_from_s3(self):
        return [
            file_name
            for file_name in os.listdir(os.path.dirname(os.path.abspath(__file__)))
            if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name))
        ]

    def copy_to_maven_local(self, dependency_from_s3, maven_local_path):
        for file_name in dependency_from_s3:
            local_file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), file_name
            )
            if os.path.isfile(local_file_path):
                shutil.copy(local_file_path, maven_local_path)

    def install(self):
        # s3_path = f"/builds/{self.version}/{self.build_id}/{self.arch}/maven/{self.get_dependency_path()}"
        maven_local_path = self.get_maven_local_path()
        if not os.path.exists(maven_local_path):
            os.makedirs(maven_local_path)
        dependency_from_s3 = self.download_from_s3()
        self.copy_to_maven_local(dependency_from_s3, maven_local_path)
