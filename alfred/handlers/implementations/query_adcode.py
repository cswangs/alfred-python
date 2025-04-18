import json
import requests
from typing import List
from alfred.entitys.result import AlfredResult
from alfred.handlers.base import Handler
from alfred.entitys.result_item import AlfredResultItem
from alfred.utils.logger import logger


class QueryAdcodeHandler(Handler):
    """查询 adcode 信息的处理器"""

    def __init__(self) -> None:
        super().__init__("query_adcode")
        self.api_url = "https://pre-yunji.amap.com/gapi/adcode/searchByAdcodeOrName"

    def handle(self, arg: List) -> AlfredResult:
        if not arg or not arg[0]:
            return AlfredResult.one("", "请输入关键词", "示例：北京市")

        keyword = arg[0]
        try:
            # 发送 API 请求
            params = {
                "keyword": keyword,
                # "extraInfo": "adcode_wkt"
            }
            response = requests.get(self.api_url, params=params)
            data = response.json()

            # 检查响应
            if data.get("code") != 0:
                return AlfredResult.one(
                    "", f"查询失败: {data.get('message')}", "请检查输入"
                )

            # 处理结果
            results = data.get("data", [])
            if not results:
                return AlfredResult.one("", "未找到匹配结果", f"关键词: {keyword}")

            # 构建结果列表
            items = []
            for item in results:
                arg_value = json.dumps(item, ensure_ascii=False)
                title = f"{item['name']} ({item['adcode']})"
                subtitle = (
                    f"级别: {item['level_type']} | 经纬度: {item['lng']},{item['lat']}"
                )
                items.append(
                    AlfredResultItem(
                        attributes={"arg": arg_value}, title=title, subtitle=subtitle
                    )
                )

            return AlfredResult(items=items)

        except Exception as e:
            logger.error(f"查询 adcode 失败: {str(e)}")
            return AlfredResult.one("", f"查询出错: {str(e)}", "请稍后重试")
