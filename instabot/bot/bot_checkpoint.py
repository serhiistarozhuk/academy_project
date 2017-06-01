import os
import pickle
from datetime import datetime

CHECKPOINT_PATH = "%s.checkpoint"


class Checkpoint(object):

    def __init__(self, bot):
        self.total_liked = bot.total_liked
        self.total_unliked = bot.total_unliked
        self.total_followed = bot.total_followed
        self.total_unfollowed = bot.total_unfollowed
        self.total_requests = bot.total_requests
        self.start_time = bot.start_time
        self.date = datetime.now()

    def dump(self):
        return (self.total_liked, self.total_unliked, self.total_followed,
                self.total_unfollowed, self.total_requests, self.start_time)


def save_checkpoint(self):
    cp = Checkpoint(self)

    with open(CHECKPOINT_PATH % self.username, 'wb') as f:
        pickle.dump(cp, f, -1)
    return True


def load_checkpoint(self):
    try:
        with open(CHECKPOINT_PATH % self.username, 'rb') as f:
            cp = pickle.load(f)
        if isinstance(cp, Checkpoint):
            return cp.dump()
        else:
            os.remove(CHECKPOINT_PATH % self.username)
    except:
        pass
    return None
