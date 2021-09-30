from collections import OrderedDict

class TestResultsComponent(OrderedDict):
    def __init__(self, component):
        self.component = component
    
    def __missing__(self,k):
        self[k] = []
        return self[k]
