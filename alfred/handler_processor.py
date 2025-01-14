import importlib
import inspect
import pkgutil
from typing import List, Type
from alfred.handlers.base import Handler
from alfred.models.result import AlfredResult
from alfred.utils.logger import logger

class HandlerProcessor:
    """命令处理器管理类"""
    
    _handlers: List[Handler] = []
    _initialized: bool = False
    
    @classmethod
    def _initialize(cls) -> None:
        """初始化并自动注册所有处理器"""
        if cls._initialized:
            return
            
        try:
            # 导入 implementations 包
            import alfred.handlers.implementations as impl_package
            
            # 遍历包中的所有模块
            for _, module_name, _ in pkgutil.iter_modules(impl_package.__path__):
                # 动态导入模块
                module = importlib.import_module(f"alfred.handlers.implementations.{module_name}")
                
                # 查找模块中的所有 Handler 子类
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) 
                        and issubclass(obj, Handler) 
                        and obj != Handler):
                        cls._handlers.append(obj())
                        logger.info(f"Registered handler: {name}")
            
            cls._initialized = True
            logger.info(f"Total handlers registered: {len(cls._handlers)}")
            
        except Exception as e:
            logger.error(f"Error initializing handlers: {e}")
            raise
    
    @classmethod
    def process(cls, command: str, arg: List) -> AlfredResult:
        """处理命令"""
        if not cls._initialized:
            cls._initialize()
            
        for handler in cls._handlers:
            if handler.command == command:
                return handler.handle(arg)
        return AlfredResult.one("未知命令", f"命令 '{command}' 不存在", "请检查命令名称")