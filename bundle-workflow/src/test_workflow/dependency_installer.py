import os
import shutil


class DependencyInstaller:
    """
    Provides functionality to copy the maven dependencies from S3 to maven local.
    """

    def __init__(self, build):
        self.build_id = build.id
        self.version = build.version
        self.arch = build.architecture

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

    def install(self, dependencies):
        file_handler = self.MavenLocalFileHandler()
        for dependency in dependencies:
            # s3_path = f"/builds/{self.version}/{self.build_id}/{self.arch}/maven/{dependency}"
            maven_local_path = os.path.join(
                os.path.expanduser("~"),
                f".m2/{self.build_id}/repository/org/opensearch/{dependency}/{self.version}/",
            )
            file_handler.copy(self.download(), maven_local_path)

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
