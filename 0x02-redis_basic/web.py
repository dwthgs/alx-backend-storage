#!/usr/bin/env python3
""" Adv task webs module """
from requests import get as r_get
from functools import wraps
from typing import Callable
import redis
redis_db = redis.Redis()
# redis_db.flushdb()


def cache(method: Callable):
    """ Caches website data """
    @wraps(method)
    def inner(*args):
        if args:
            url = args[0]
            redis_db.incr(f"count:{url}")

            cached_data = redis_db.get(url)
            if cached_data:
                return str(cached_data, 'UTF-8')

            html_response = method(url)
            redis_db.set(url, html_response, 10)
            return html_response

    return inner


@cache
def get_page(url: str) -> str:
    """ Runs a GET request on a given URL """
    if type(url) is str:
        req = r_get(url)
        return req.text
