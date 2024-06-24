def 进制转换_十进制转三十二进制(十进制数):
    """
    将十进制数转换为三十二进制字符串。

    参数:
        十进制数 (int): 要转换的十进制整数。

    返回:
        str: 转换后的三十二进制字符串，如果输入不是有效的十进制数则返回 None。

    示例使用:
        三十二进制字符串 = 进制转换_十进制转三十二进制(12345)
        print("转换后的三十二进制字符串:", 三十二进制字符串)
    """
    try:
        # 检查输入是否为非负整数
        if 十进制数 < 0 or not isinstance(十进制数, int):
            return None

        # 定义32进制的字符集
        字符集 = '0123456789abcdefghijklmnopqrstuv'
        if 十进制数 == 0:
            return '0'
        三十二进制字符串 = ''
        while 十进制数 > 0:
            十进制数, 余数 = divmod(十进制数, 32)
            三十二进制字符串 = 字符集[余数] + 三十二进制字符串
        return 三十二进制字符串
    except Exception:
        return None