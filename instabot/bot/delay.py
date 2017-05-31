import time
import random


def add_dispersion(delay_value):
    return delay_value * 3 / 4 + delay_value * random.random() / 2


def like_delay(bot):
    time.sleep(add_dispersion(bot.like_delay))


def unfollow_delay(bot):
    time.sleep(add_dispersion(bot.unfollow_delay))


def error_delay(bot):
    time.sleep(10)


def small_delay(bot):
    time.sleep(add_dispersion(3))


def very_small_delay(bot):
    time.sleep(add_dispersion(0.7))
