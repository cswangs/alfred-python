# -*- coding: utf-8 -*-
import itertools
import os
import plistlib
import unicodedata
import sys

from xml.etree.ElementTree import Element, SubElement, tostring

from alfred.utils.logger import logger

"""
You should run your script via /bin/bash with all escape options ticked.
The command line should be

python yourscript.py "{query}" arg2 arg3 ...
"""
UNESCAPE_CHARACTERS = """ ;()"""

try:
    with open("info.plist", "rb") as fp:
        preferences = plistlib.load(fp)
except FileNotFoundError:
    try:
        with open("workflow/info.plist", "rb") as fp:
            preferences = plistlib.load(fp)
    except FileNotFoundError:
        logger.error("错误：info.plist 文件未找到！")
        preferences = {}
except Exception as e:
    preferences = {}
    logger.error(f"读取 info.plist 时出错: {e}")

# logger.info(f"读取 info.plist: {preferences}")
bundleid = preferences.get("bundleid", "none")


def args(characters=None):
    return tuple(unescape(decode(arg), characters) for arg in sys.argv[1:])


def config():
    return _create("config")


def decode(s):
    return unicodedata.normalize("NFC", s.decode("utf-8"))


def uid(uid):
    return "-".join(map(str, (bundleid, uid)))  # 替换 unicode 为 str


def unescape(query, characters=None):
    for character in UNESCAPE_CHARACTERS if (characters is None) else characters:
        query = query.replace("\\%s" % character, character)
    return query


def work(volatile):
    path = {
        True: "~/Library/Caches/com.runningwithcrayons.Alfred-2/Workflow Data",
        False: "~/Library/Application Support/Alfred 2/Workflow Data",
    }[bool(volatile)]
    return _create(os.path.join(os.path.expanduser(path), bundleid))


def write(text):
    sys.stdout.write(text)


def _create(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.access(path, os.W_OK):
        raise IOError("No write access: %s" % path)
    return path
