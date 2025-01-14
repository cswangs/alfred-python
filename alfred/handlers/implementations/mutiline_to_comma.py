from typing import List
from alfred.models.result import AlfredResult
from alfred.handlers.base import Handler


class MutilineToComma(Handler):
    def __init__(self) -> None:
        super().__init__("multiline_to_comma")

    def handle(self, arg: List) -> AlfredResult:
        input_str = arg[0]
        quote_type = arg[1] if len(arg) > 1 else 'single_quota'
        if quote_type =='single_quota':
            quotaStr = "'"
        elif quote_type =='double_quota':
            quotaStr = '"'
        elif quote_type =='empty':
            quotaStr = ""
            
        values: List[str] = [f"{quotaStr}{line.strip()}{quotaStr}" for line in input_str.split('\n') if line.strip()]
        if not values:
            return AlfredResult.one("", "请输入有效值", "输入为空")
        value = f"{','.join(values)}"
        return AlfredResult.one(value, value, "多行字符串转为逗号分隔")