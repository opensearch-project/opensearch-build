import abc

from test_workflow.test_recorder.test_result_data import TestResultData


class LogRecorder(abc.ABC):
    """
    Abstract class for all types of log recording
    """

    @abc.abstractmethod
    def save_test_result_data(self, test_result_data: TestResultData) -> None:
        """
        Defines how the result data is are recorded
        """
        pass
