"""
Class that will contain key words to start command and then actions for
command to perform
"""
import inspect

class Command(object):
    def __init__(self):
        self.keywords = list()

    def hasKeyword(self, keyword):
        return keyword in self.keywords
    
    @classmethod
    def needsPassword(cls):
        inputs = inspect.getargspec(cls.__init__)
        if len(inputs[0]) == 1:
            return False
        else:
            return True

    def run(self,commandlist):
        pass
