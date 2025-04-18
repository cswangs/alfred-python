from typing import Optional
from xml.etree.ElementTree import Element, SubElement
from lxml import etree


class AlfredResultItem:
    """Alfred 工作流结果项"""

    def __init__(
        self,
        attributes: dict = None,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        icon: Optional[str] = None,
    ) -> None:
        """
        初始化结果项

        Args:
            arg: 参数值
            title: 标题
            subtitle: 副标题
        """
        self.attributes = attributes
        self.title = title
        self.subtitle = subtitle
        self.icon = icon

    @classmethod
    def unicode(cls, value):
        try:
            items = value.items()  # 修改 iteritems 为 items
        except AttributeError:
            return str(value)  # 替换 unicode 为 str
        else:
            return dict(map(str, item) for item in items)

    def to_xml(self):
        """
        使用 lxml 构建 XML 元素
        """
        # 创建根元素 <item>，并添加 attributes 作为属性
        item = etree.Element("item", self.unicode(self.attributes))

        # 遍历 title, subtitle, icon 属性
        for attribute in ("title", "subtitle", "icon"):
            value = getattr(self, attribute)
            if value is None:
                continue
            try:
                # 如果 value 是一个元组，解包为 value 和 attributes
                (value, attributes) = value
            except:
                # 如果不是元组，attributes 默认为空字典
                attributes = {}

            # 创建子元素并设置文本内容
            etree.SubElement(item, attribute, self.unicode(attributes)).text = str(
                value
            )
        return item
