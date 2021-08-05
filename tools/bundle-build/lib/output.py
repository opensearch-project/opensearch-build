import os

class BuildOutput:
    def __init__(self):
        self._dest = os.path.join(os.getcwd(), 'artifacts')
        self.__ensure_dest()

    def dest(self):
        return self._dest

    def __ensure_dest(self):
        if os.path.exists(self.dest()):
            raise Exception(f'Directory exists: {self.dest()}')
        os.makedirs(self.dest())
