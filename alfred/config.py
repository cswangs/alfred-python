from dataclasses import dataclass
from typing import Dict, Any
import os

@dataclass
class Config:
    """应用配置类"""
    # 日志配置
    LOG_ENABLED: bool = os.getenv("ALFRED_LOG_ENABLED", "true").lower() == "false"
    LOG_LEVEL: str = os.getenv("ALFRED_LOG_LEVEL", "INFO")
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 其他配置
    DEFAULT_TITLE: str = "Default Title"
    DEFAULT_SUBTITLE: str = "Default Subtitle"
    DEBUG: bool = os.getenv("ALFRED_DEBUG", "false").lower() == "true"

    ERROR_MESSAGES = {
        "command_missing": "请输入命令",
        "command_not_found": "未找到命令: {}",
        "execution_error": "执行出错: {}"
    }