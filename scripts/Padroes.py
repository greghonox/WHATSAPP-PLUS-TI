from datetime import datetime

class DateTime():
    def __init__(self):
        self.format = '%d/%m/%Y %H:%M:%S'

    def __repr__(self): return datetime.now().strftime(self.format)

    def __str__(self): return datetime.now().strftime(self.format)

    def __add__(self, v):
        return self.__repr__() +' '+ v
