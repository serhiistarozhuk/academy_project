import datetime
import atexit
import signal

from ..api import API

from .bot_get import get_media_owner, get_your_medias, get_user_medias
from .bot_get import get_hashtag_medias, get_user_info
from .bot_get import convert_to_user_id
from .bot_get import get_media_info

from .bot_like import like, like_medias, like_user, like_users
from .bot_like import like_hashtag

from .bot_checkpoint import save_checkpoint, load_checkpoint

from .bot_filter import filter_medias, check_media, filter_users, check_user
from .bot_filter import check_not_bot


class Bot(API):

    def __init__(self,
                 max_likes_per_day=1000,
                 max_unlikes_per_day=1000,
                 max_follows_per_day=350,
                 max_unfollows_per_day=350,
                 max_comments_per_day=100,
                 max_blocks_per_day=100,
                 max_unblocks_per_day=100,
                 max_likes_to_like=100,
                 filter_users=True,
                 max_followers_to_follow=2000,
                 min_followers_to_follow=10,
                 max_following_to_follow=2000,
                 min_following_to_follow=10,
                 max_followers_to_following_ratio=10,
                 max_following_to_followers_ratio=2,
                 min_media_count_to_follow=3,
                 like_delay=10,
                 unlike_delay=10,
                 follow_delay=30,
                 unfollow_delay=30,
                 comment_delay=60,
                 stop_words=['shop', 'store', 'free']):
        super(self.__class__, self).__init__()

        self.total_liked = 0
        self.total_unliked = 0
        self.total_followed = 0
        self.total_unfollowed = 0
        self.total_commented = 0
        self.total_blocked = 0
        self.total_unblocked = 0
        self.start_time = datetime.datetime.now()

        # limits - follow
        self.filter_users = filter_users
        self.max_likes_per_day = max_likes_per_day
        self.max_unlikes_per_day = max_unlikes_per_day
        self.max_follows_per_day = max_follows_per_day
        self.max_unfollows_per_day = max_unfollows_per_day
        self.max_comments_per_day = max_comments_per_day
        self.max_blocks_per_day = max_blocks_per_day
        self.max_unblocks_per_day = max_unblocks_per_day
        self.max_likes_to_like = max_likes_to_like
        self.max_followers_to_follow = max_followers_to_follow
        self.min_followers_to_follow = min_followers_to_follow
        self.max_following_to_follow = max_following_to_follow
        self.min_following_to_follow = min_following_to_follow
        self.max_followers_to_following_ratio = max_followers_to_following_ratio
        self.max_following_to_followers_ratio = max_following_to_followers_ratio
        self.min_media_count_to_follow = min_media_count_to_follow
        self.stop_words = stop_words

        # delays
        self.like_delay = like_delay
        self.unfollow_delay = unfollow_delay

        # current following
        self.following = []

        self.logger.info('Instabot Started')

    def version(self):
        try:
            from pip._vendor import pkg_resources
        except ImportError:
            import pkg_resources
        return next((p.version for p in pkg_resources.working_set if p.project_name.lower() == 'instabot'), "No match")

    def logout(self):
        save_checkpoint(self)
        super(self.__class__, self).logout()
        self.logger.info("Bot stopped. "
                         "Worked: %s" % (datetime.datetime.now() - self.start_time))
        self.print_counters()

    def login(self, **args):
        super(self.__class__, self).login(**args)
        self.prepare()
        signal.signal(signal.SIGTERM, self.logout)
        atexit.register(self.logout)

    def prepare(self):
        storage = load_checkpoint(self)
        if storage is not None:
            self.total_liked, self.total_unliked, self.total_followed, self.total_unfollowed, self.total_requests, self.start_time = storage

    def print_counters(self):
        if self.total_liked:
            self.logger.info("Total liked: %d" % self.total_liked)

    # getters

    def get_your_medias(self):
        return get_your_medias(self)

    def get_user_medias(self, user_id, filtration=True):
        return get_user_medias(self, user_id, filtration)

    def get_hashtag_medias(self, hashtag, filtration=True):
        return get_hashtag_medias(self, hashtag, filtration)

    def get_media_info(self, media_id):
        return get_media_info(self, media_id)

    def get_user_info(self, user_id):
        return get_user_info(self, user_id)

    def get_media_owner(self, media):
        return get_media_owner(self, media)

    def convert_to_user_id(self, usernames):
        return convert_to_user_id(self, usernames)

    # like

    def like(self, media_id):
        return like(self, media_id)

    def like_medias(self, media_ids):
        return like_medias(self, media_ids)

    def like_user(self, user_id, amount=None):
        return like_user(self, user_id, amount)

    def like_hashtag(self, hashtag, amount=None):
        return like_hashtag(self, hashtag, amount)

    def like_users(self, user_ids, nlikes=None):
        return like_users(self, user_ids, nlikes)

    # filter

    def filter_medias(self, media_items, filtration=True, quiet=False):
        return filter_medias(self, media_items, filtration, quiet)

    def check_media(self, media):
        return check_media(self, media)

    def check_user(self, user, filter_closed_acc=False):
        return check_user(self, user, filter_closed_acc)

    def check_not_bot(self, user):
        return check_not_bot(self, user)

    def filter_users(self, user_id_list):
        return filter_users(self, user_id_list)
