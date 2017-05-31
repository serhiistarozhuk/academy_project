import datetime


def reset_counters(bot):
    bot.total_liked = 0
    bot.total_unliked = 0
    bot.total_unfollowed = 0
    bot.start_time = datetime.datetime.now()


def reset_if_day_passed(bot):
    current_date = datetime.datetime.now()
    passed_days = (current_date.date() - bot.start_time.date()).days
    if passed_days != 0:
        reset_counters(bot)


def check_if_bot_can_unfollow(bot):
    reset_if_day_passed(bot)
    return bot.max_unfollows_per_day - bot.total_unfollowed > 0


def check_if_bot_can_unlike(bot):
    reset_if_day_passed(bot)
    return bot.max_unlikes_per_day - bot.total_unliked > 0


def check_if_bot_can_like(bot):
    reset_if_day_passed(bot)
    return bot.max_likes_per_day - bot.total_liked > 0
