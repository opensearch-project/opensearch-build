# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc


class Service(abc.ABC):
    """
    Abstract base class for all types of test clusters.
    """

    @abc.abstractmethod
    def start(self):
        """
        Start a service.
        """
        pass

    @abc.abstractmethod
    def terminate(self):
        """
        Terminate this service.
        """
        pass

    @abc.abstractmethod
    def endpoint(self):
        """
        Get the endpoint that this service is listening on, e.g. 'localhost' or 'some.ip.address'.
        """
        pass

    @abc.abstractmethod
    def port(self):
        """
        Get the port that this service is listening on.
        """
        pass
