import os
import shutil


class DependencyInstaller:
    """
    Provides functionality to copy the maven dependencies from S3 to maven local.
    """

    def __init__(self, build_id, dependency_name, version, arch):
        self.build_id = build_id
        self.dependency_name = dependency_name
        self.version = version
        self.arch = arch
        self.dependency_path = f"org/opensearch/{self.dependency_name}/{self.version}/"
        self.maven_local_path = os.path.join(
            os.path.expanduser("~"), ".m2/repository/", self.dependency_path
        )

    # TODO: This is currently a stubbed function which returns files from the current directory,
    # to be replaced after it is implemented
    def download(self):
        return [
            file_name
            for file_name in os.listdir(os.path.dirname(os.path.abspath(__file__)))
            if os.path.isfile(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
            )
        ]

    def install(self):
        # s3_path = f"/builds/{self.version}/{self.build_id}/{self.arch}/maven/{self.dependency_path()}"
        file_handler = self.MavenLocalFileHandler()
        file_handler.copy(self.download(), self.maven_local_path)

    class MavenLocalFileHandler:
        """
        Copies given dependencies to maven local.
        """

        def copy(self, dependency_from_s3, maven_local_path):
            os.makedirs(maven_local_path, exist_ok=True)
            for file_name in dependency_from_s3:
                local_file_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), file_name
                )
                shutil.copy(local_file_path, maven_local_path)
