def 进制转换_二进制转十进制(二进制字符串):
    """
    将二进制字符串转换为十进制整数。

    参数:
        二进制字符串 (str): 要转换的二进制字符串。

    返回:
        int: 转换后的十进制整数，如果输入不是有效的二进制字符串则返回 None。

    示例使用:
        十进制整数 = 进制转换_二进制转十进制('110010101011')
        print(十进制整数)  # 输出：'3243'
    """
    try:
        十进制整数 = int(二进制字符串, 2)
        return 十进制整数
    except Exception:
        return None