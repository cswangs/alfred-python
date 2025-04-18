import calendar
from datetime import timedelta
import json
import requests
from typing import List

from tzlocal import get_localzone
from alfred import alfred
from alfred.entitys.result import AlfredResult
from alfred.handlers.base import Handler
from alfred.entitys.result_item import AlfredResultItem
from alfred.utils.logger import logger
from delorean import parse, epoch, Delorean


class QueryAdcodeHandler(Handler):
    """查询 adcode 信息的处理器"""

    def __init__(self) -> None:
        super().__init__("df")
        self.tz = str(get_localzone())

    def handle(self, arg: List) -> AlfredResult:
        if not arg or not arg[0]:
            return AlfredResult.one(
                "", "请输入关键词", "示例：1735660800000 or 2025 01 01"
            )
        keyword = arg[0]
        value = self.parse_query_value(keyword)
        results = self.alfred_items_for_value(value)
        return AlfredResult(items=results)

    def parse_query_value(self, query_str):
        """Return value for the query string"""

        try:
            query_str = str(query_str).strip("\"' ")
            if query_str == "now":
                d = Delorean(timezone=self.tz)
            elif query_str.startswith("y"):
                d = Delorean(Delorean(timezone=self.tz).midnight)
                d -= timedelta(days=len(query_str))
            elif query_str.startswith("t"):
                d = Delorean(Delorean(timezone=self.tz).midnight)
                d += timedelta(days=len(query_str) - 1)
            else:
                # Parse datetime string or timestamp
                try:
                    ts = float(query_str)
                    if ts >= 1000000000000:
                        ts /= 1000
                    d = epoch(float(ts))
                    d.shift(self.tz)
                except ValueError:
                    d = parse(str(query_str), self.tz, dayfirst=False)
        except (TypeError, ValueError):
            d = None
        return d

    def alfred_items_for_value(self, value):
        """
        Given a delorean datetime object, return a list of
        alfred items for each of the results
        """

        index = 0
        results = []
        subtitle = self.tz + " Timestamp"
        icon = "B4BA90C2-1A7B-4592-BB12-C675D39027CC.png"

        # First item as timestamp
        unx_value = calendar.timegm(value.datetime.utctimetuple())
        item_value = unx_value * 1000

        results.append(
            AlfredResultItem(
                title=str(unx_value),
                subtitle=subtitle,
                attributes={
                    "uid": alfred.uid(index),
                    "arg": unx_value,
                },
                icon=icon,
            )
        )
        index += 1
        results.append(
            AlfredResultItem(
                title=str(item_value),
                subtitle=subtitle,
                attributes={
                    "uid": alfred.uid(index),
                    "arg": item_value,
                },
                icon=icon,
            )
        )
        index += 1
        # Various formats
        formats = [
            # 1937-01-01 12:00:27
            ("%Y-%m-%d %H:%M:%S", ""),
            # 19 May 2002 15:21:36
            ("%d %b %Y %H:%M:%S", ""),
            # Sun, 19 May 2002 15:21:36
            ("%a, %d %b %Y %H:%M:%S", ""),
            # 1937-01-01T12:00:27
            ("%Y-%m-%dT%H:%M:%S", ""),
            # 1996-12-19T16:39:57-0800
            ("%Y-%m-%dT%H:%M:%S%z", ""),
        ]
        for format, description in formats:
            item_value = value.datetime.strftime(format)
            results.append(
                AlfredResultItem(
                    title=str(item_value),
                    subtitle=description,
                    attributes={
                        "uid": alfred.uid(index),
                        "arg": item_value,
                    },
                    icon=icon,
                )
            )
            index += 1

        return results
