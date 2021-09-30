class TestResultsSuite():

    def __init__(self):
        self.all_results = list()

    def append(self, test_result):
        self.all_results.append(test_result)
    
    def log(self):
        for result in self.all_results:
            for component, logs in result.items():
                for log in logs:
                    print(log)


    #def status()        

