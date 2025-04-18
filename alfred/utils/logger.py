import logging
import sys
from typing import Optional
from alfred.config import Config

class Logger:
    """日志管理类"""
    
    _instance: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """获取日志实例（单例模式）"""
        if cls._instance is None:
            logger = logging.getLogger("alfred")
            
            # 检查是否是通过 python -m 方式运行
            is_module_run = any(arg.endswith('alfred.main') for arg in sys.argv[0:1])
            is_module_run = is_module_run or any(arg.endswith('alfred/main.py') for arg in sys.argv[0:1])
            if is_module_run or Config.LOG_ENABLED:
                logger.setLevel(Config.LOG_LEVEL)
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(
                    logging.Formatter(Config.LOG_FORMAT)
                )
                logger.addHandler(console_handler)
            else:
                # 禁用日志
                logger.disabled = True
                logger.addHandler(logging.NullHandler())
            
            cls._instance = logger
        
        return cls._instance

# 便捷访问
logger = Logger.get_logger()