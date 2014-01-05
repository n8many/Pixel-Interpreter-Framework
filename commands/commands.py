"""
Class that will contain key words to start command and then actions for
command to perform
"""

class Commands(object):
    def __init__(self):
        keywords = list()

    def hasKeyword(self, keyword):
        return keyword in keywords
