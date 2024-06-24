from bs4 import BeautifulSoup


def html_通用查找(html文本, 标签名, 属性类型, 属性值):
    """
    从给定的HTML文本中，根据标签名和属性类型及属性值查找元素，并返回包含这些元素的列表。

    参数:
        html文本 (str): HTML 文本
        标签名 (str): 要查找的标签名
        属性类型 (str): 要查找的属性类型（例如，class、id、src、href、alt、title、name、type 和 placeholder）
        属性值 (str): 要查找的属性值

    返回:
        list: 包含符合条件的元素的列表

    示例：
        查找结果 = html_通用查找(响应文本, "div", "class","ZPGj85")
        print(查找结果)
    """
    try:
        soup = BeautifulSoup(html文本, 'html.parser')
        属性 = {属性类型: 属性值}
        元素列表 = soup.find_all(标签名, 属性)
        return 元素列表
    except Exception:
        return []
