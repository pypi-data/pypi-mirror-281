def 文本_取文本指定次数出现的位置(文本, 查找的文本, 次数):
    """
    返回指定文本中指定子串出现的指定次数后的位置。

    参数：
    文本 (str): 要搜索的文本。
    查找的文本 (str): 要查找的子串。
    次数 (int): 子串第几次出现的位置

    返回值：
    int: 子串指定次数出现后的位置索引，如果没有找到或者次数超过实际出现次数返回-1。

    使用示例：
    文本_取文本指定次数出现的位置("ABABABABABA", "A", 3)
    以上参数传递的意思就是，寻找ABABABABABA 这个字符串内第三个A 出现的位置，
    """
    try:
        # 初始化计数器和位置索引
        计数器 = 0
        位置索引 = -1

        # 使用循环查找指定次数后的位置
        while 计数器 < 次数:
            位置索引 = 文本.find(查找的文本, 位置索引 + 1)
            if 位置索引 == -1:
                break
            计数器 += 1

        return 位置索引
    except Exception:
        return -1