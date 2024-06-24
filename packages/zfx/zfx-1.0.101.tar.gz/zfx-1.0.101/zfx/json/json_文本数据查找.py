import json
import jsonpath


def json_文本数据查找(数据对象, 层级路径, 键, 值):
    """
    使用说明：
    1、数值数据查找，按照指定的层级目录下开始进行查找，提取所有符合条件的目标所在层级详细信息。

    2、层级名称不固定可用*号代替。遇到层级路径中如果包含列表就用索引选择[0]或[*]，比如：edges[0]，

    3、假设想要查找的数据在第五层内，那么层级路径只需要写到第四层（如果层级路径也写到第五层将失去查找的意义）

    参数:
    数据对象 (dict_字典 或 str_字符串): Python 字典对象或 json 字符串。
    层级路径 (str_字符串): 层级路径。
    键 (str_字符串): 要查找的键。
    值 (str_字符串): 要查找的值。

    返回:
    list: 匹配的数据列表，如果没有匹配或异常则返回空列表。

    使用示例：
    # 提取所有 'name' 为 'zeng' 的所在层级信息
    查找结果 = json_文本数据查找(数据对象, "data.第一层.第二层", "name", "zeng")
    print(查找结果)
    """
    try:
        # 如果传入的是 json 字符串，则解析为 Python 字典
        if isinstance(数据对象, str):
            数据对象 = json.loads(数据对象)

        # 构建 JSONPath 表达式，根据指定键和值查找匹配的数据
        表达式 = f"$.{层级路径}[?(@.{键} == '{值}')]"

        # 执行 JSONPath 查询
        匹配结果 = jsonpath.jsonpath(数据对象, 表达式)

        return 匹配结果 if 匹配结果 else []
    except Exception:
        return []