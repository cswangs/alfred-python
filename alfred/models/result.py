from typing import List, Optional
from lxml import etree
from alfred.models.result_item import AlfredResultItem

class AlfredResult:
    """处理 Alfred 工作流的结果类"""
    
    def __init__(self, items: Optional[List[AlfredResultItem]] = None) -> None:
        """
        初始化 AlfredResult
        
        Args:
            items: Alfred 结果项列表
        """
        self.items = items or []

    @staticmethod
    def one(arg: str, title: str, subtitle: str = '') -> 'AlfredResult':
        """
        创建单个结果项
        
        Args:
            arg: 参数值
            title: 标题
            subtitle: 副标题
        
        Returns:
            AlfredResult 实例
        """
        return AlfredResult(items=[AlfredResultItem(arg=arg, title=title, subtitle=subtitle)])

    def to_xml(self) -> str:
        """
        将结果转换为 Alfred 可识别的 XML 格式
        
        Returns:
            XML 字符串
        """
        root = etree.Element("items")
        for item in self.items:
            item_elem = etree.SubElement(root, "item")
            item_elem.set("arg", str(item.arg))
            
            title_elem = etree.SubElement(item_elem, "title")
            title_elem.text = str(item.title or "Default Title")
            
            subtitle_elem = etree.SubElement(item_elem, "subtitle")
            subtitle_elem.text = str(item.subtitle or "Default Subtitle")

        return etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode() 