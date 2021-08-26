import os


class TestUtils:
    def get_test_dependencies():
        test_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../../src/test_workflow"
        )
        return [
            file_name
            for file_name in os.listdir(test_dir)
            if os.path.isfile(os.path.join(test_dir, file_name))
        ]
