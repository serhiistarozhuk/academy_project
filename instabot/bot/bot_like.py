from tqdm import tqdm
from . import limits
from . import delay


def like(self, media_id):
    if limits.check_if_bot_can_like(self):
        delay.like_delay(self)
        if super(self.__class__, self).like(media_id):
            self.total_liked += 1
            return True
    else:
        self.logger.info("Out of likes for today.")
    return False


def like_medias(self, medias):
    broken_items = []
    if len(medias) == 0:
        self.logger.info("Nothing to like.")
        return broken_items
    self.logger.info("Going to like %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.like(media):
            delay.error_delay(self)
            broken_items = medias[medias.index(media):]
            break
    self.logger.info("DONE: Total liked %d medias." % self.total_liked)
    return broken_items


def like_user(self, user_id, amount=None):
    if not self.check_user(user_id, filter_closed_acc=True):
        return False
    self.logger.info("Liking user_%s's feed:" % user_id)
    user_id = self.convert_to_user_id(user_id)
    medias = self.get_user_medias(user_id)
    if not medias:
        self.logger.info(
            "None medias received: account is closed or medias have been filtered.")
        return False
    return self.like_medias(medias[:amount])


def like_users(self, user_ids, nlikes=None):
    for user_id in user_ids:
        self.like_user(user_id, amount=nlikes)


def like_hashtag(self, hashtag, amount=None):
    """ Likes last medias from hashtag """
    self.logger.info("Going to like media with hashtag #%s." % hashtag)
    medias = self.get_hashtag_medias(hashtag)
    return self.like_medias(medias[:amount])
