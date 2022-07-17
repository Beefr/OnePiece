
from message import Message


class MultiLineMessage(object):


    def __init__(self):
        self._myMessages=[]
        
    @property
    def myMessages(self):
        return self._myMessages

    def __add__(self, messages):
        if isinstance(messages, Message):
            self._myMessages.append([messages])
        elif isinstance(messages, MultiLineMessage):
            self._myMessages.extend(messages.myMessages)
        elif isinstance(messages, str):
            self._myMessages.append([Message(messages)])
        elif isinstance(messages, list):
            self._myMessages.extend(messages)


    def __mul__(self, message):
        if isinstance(message, Message):
            self._myMessages[-1].append(message)
        elif isinstance(message, str):
            self._myMessages[-1].append(Message(message))