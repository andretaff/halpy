import uuid
import random
class Rand64(object):
    """description of class"""
    def next(self):
        return int(random.getrandbits(64)) ## uuid.uuid4().int & (1<<64)-1


