import random
from tqdm import tqdm

from . import delay


def get_media_owner(self, media_id):
    self.mediaInfo(media_id)
    try:
        return str(self.LastJson["items"][0]["user"]["pk"])
    except:
        return False


def get_your_medias(self):
    self.getSelfUserFeed()
    return self.filter_medias(self.LastJson["items"], False)


def get_user_medias(self, user_id, filtration=True):
    user_id = self.convert_to_user_id(user_id)
    self.getUserFeed(user_id)
    if self.LastJson["status"] == 'fail':
        self.logger.warning("This is a closed account.")
        return []
    return self.filter_medias(self.LastJson["items"], filtration)


def get_hashtag_medias(self, hashtag, filtration=True):
    if not self.getHashtagFeed(hashtag):
        self.logger.warning("Error while getting hashtag feed.")
        return []
    return self.filter_medias(self.LastJson["items"], filtration)


def get_media_info(self, media_id):
    self.mediaInfo(media_id)
    return self.LastJson["items"]


def get_hashtag_users(self, hashtag):
    users = []
    self.getHashtagFeed(hashtag)
    for i in self.LastJson['items']:
        users.append(str(i['user']['pk']))
    return users


def get_user_info(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    self.getUsernameInfo(user_id)
    if 'user' not in self.LastJson:
        return False
    return self.LastJson['user']


def convert_to_user_id(self, smth):
    smth = str(smth)
    if not smth.isdigit():
        if smth[0] == "@":  # cut first @
            smth = smth[1:]
        smth = self.get_userid_from_username(smth)
        delay.very_small_delay(self)
    # if type is not str than it is int so user_id passed
    return smth
