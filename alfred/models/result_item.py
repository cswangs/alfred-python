from typing import Optional

class AlfredResultItem:
    """Alfred 工作流结果项"""
    
    def __init__(
        self, 
        arg: Optional[str] = None,
        title: Optional[str] = None,
        subtitle: Optional[str] = None
    ) -> None:
        """
        初始化结果项
        
        Args:
            arg: 参数值
            title: 标题
            subtitle: 副标题
        """
        self.arg = arg
        self.title = title
        self.subtitle = subtitle 