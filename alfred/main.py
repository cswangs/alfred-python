import sys
from typing import Optional
from alfred.models.result import AlfredResult
from alfred.handler_processor import HandlerProcessor

from alfred.utils.logger import logger

def main() -> None:
    """主函数入口"""
    try:
        if len(sys.argv) <= 1:
            result = AlfredResult.one("请输入命令", "请输入命令", "命令参数缺失")
        else:
            command = sys.argv[1]
            result = HandlerProcessor.process(command, sys.argv[2:])
        logger.info("Starting workflow...")
        print(result.to_xml())
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}", exc_info=True)
        result = AlfredResult.one("系统错误", str(e), "程序执行出错")
        print(result.to_xml())

if __name__ == "__main__":
    main() 