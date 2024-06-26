#!/usr/bin/env python3
from __future__ import annotations

import difflib
import os
import re
from collections.abc import AsyncIterator
from http.cookies import SimpleCookie
from urllib.parse import urlparse

from requests.utils import cookiejar_from_dict


### HELP FUNCTION ###
def parse_cookie_string(cookie_string):
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    cookies_dict = {k: m.value for k, m in cookie.items()}
    return cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)


_no_elapse_chars = re.compile(r"([「」『』《》“”'\"()（）]|(?<!-)-(?!-))", re.UNICODE)


def calculate_tts_elapse(text: str) -> float:
    # for simplicity, we use a fixed speed
    speed = 4.5  # this value is picked by trial and error
    # Exclude quotes and brackets that do not affect the total elapsed time
    return len(_no_elapse_chars.sub("", text)) / speed


_ending_punctuations = ("。", "？", "！", "；", ".", "?", "!", ";")


async def split_sentences(text_stream: AsyncIterator[str]) -> AsyncIterator[str]:
    cur = ""
    async for text in text_stream:
        cur += text
        if cur.endswith(_ending_punctuations):
            yield cur
            cur = ""
    if cur:
        yield cur


### for edge-tts utils ###
def find_key_by_partial_string(dictionary: dict[str, str], partial_key: str) -> str:
    for key, value in dictionary.items():
        if key in partial_key:
            return value


def validate_proxy(proxy_str: str) -> bool:
    """Do a simple validation of the http proxy string."""

    parsed = urlparse(proxy_str)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Proxy scheme must be http or https")
    if not (parsed.hostname and parsed.port):
        raise ValueError("Proxy hostname and port must be set")

    return True


# 模糊搜索
def fuzzyfinder(user_input, collection):
    return difflib.get_close_matches(user_input, collection, 10, cutoff=0.1)


# 歌曲排序
def custom_sort_key(s):
    # 使用正则表达式分别提取字符串的数字前缀和数字后缀
    prefix_match = re.match(r"^(\d+)", s)
    suffix_match = re.search(r"(\d+)$", s)

    numeric_prefix = int(prefix_match.group(0)) if prefix_match else None
    numeric_suffix = int(suffix_match.group(0)) if suffix_match else None

    if numeric_prefix is not None:
        # 如果前缀是数字，先按前缀数字排序，再按整个字符串排序
        return (0, numeric_prefix, s)
    elif numeric_suffix is not None:
        # 如果后缀是数字，先按前缀字符排序，再按后缀数字排序
        return (1, s[: suffix_match.start()], numeric_suffix)
    else:
        # 如果前缀和后缀都不是数字，按字典序排序
        return (2, s)


# fork from https://gist.github.com/dougthor42/001355248518bc64d2f8
def walk_to_depth(root, depth=None, *args, **kwargs):
    """
    Wrapper around os.walk that stops after going down `depth` folders.
    I had my own version, but it wasn't as efficient as
    http://stackoverflow.com/a/234329/1354930, so I modified to be more
    similar to nosklo's answer.
    However, nosklo's answer doesn't work if topdown=False, so I kept my
    version.
    """
    # Let people use this as a standard `os.walk` function.
    if depth is None:
        return os.walk(root, *args, **kwargs)

    # remove any trailing separators so that our counts are correct.
    root = root.rstrip(os.path.sep)

    def main_func(root, depth, *args, **kwargs):
        """Faster because it skips traversing dirs that are too deep."""
        root_depth = root.count(os.path.sep)
        for dirpath, dirnames, filenames in os.walk(root, *args, **kwargs):
            yield (dirpath, dirnames, filenames)

            # calculate how far down we are.
            current_folder_depth = dirpath.count(os.path.sep)
            if current_folder_depth >= root_depth + depth:
                del dirnames[:]

    def fallback_func(root, depth, *args, **kwargs):
        """Slower, but works when topdown is False"""
        root_depth = root.count(os.path.sep)
        for dirpath, dirnames, filenames in os.walk(root, *args, **kwargs):
            current_folder_depth = dirpath.count(os.path.sep)
            if current_folder_depth <= root_depth + depth:
                yield (dirpath, dirnames, filenames)

    # there's gotta be a better way do do this...
    try:
        if args[0] is False:
            yield from fallback_func(root, depth, *args, **kwargs)
            return
        else:
            yield from main_func(root, depth, *args, **kwargs)
            return
    except IndexError:
        pass

    try:
        if kwargs["topdown"] is False:
            yield from fallback_func(root, depth, *args, **kwargs)
            return
        else:
            yield from main_func(root, depth, *args, **kwargs)
            return
    except KeyError:
        yield from main_func(root, depth, *args, **kwargs)
        return
