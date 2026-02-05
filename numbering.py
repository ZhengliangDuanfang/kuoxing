import re

all_in_number = "零一二三四五六七八九〇壹两贰叁肆伍陆柒捌玖百佰十拾又有"
odd_in_code = "甲乙丙丁戊己庚辛壬癸"
even_in_code = "子丑寅卯辰巳午未申酉戌亥"
all_in_code = odd_in_code + even_in_code

def number_to_int(text):
    """
    将"x百x十又x"格式的中文数字转换为整数
    """
    # 定义中文数字映射
    digit_map = {
        '零': 0, '〇': 0,
        '一': 1, '壹': 1,
        '二': 2, '两': 2, '贰': 2,
        '三': 3, '叁': 3,
        '四': 4, '肆': 4,
        '五': 5, '伍': 5,
        '六': 6, '陆': 6,
        '七': 7, '柒': 7,
        '八': 8, '捌': 8,
        '九': 9, '玖': 9
    }
    # 正则表达式匹配模式
    # 支持：x百x十x、x百x十、x百零x、x百x、x十x、x百x十又x等
    pattern = r'^([' + ''.join(digit_map.keys()) + r']?[百佰])?' \
              r'([' + ''.join(digit_map.keys()) + r']?[十拾])?' \
              r'([又有]?[' + ''.join(digit_map.keys()) + r'])?$'
    
    match = re.match(pattern, text)
    if not match:
        match2 = re.match(r'^(' + '|'.join(digit_map.keys()) + r')$', text)
        if not match2:
            return -1
        else:
            result = digit_map[match2.group(1)]
            return result
    
    groups = match.groups()
    result = 0
    if groups[0]:  # 百位数字
        if len(groups[0]) == 2:
            result += digit_map[groups[0][0]] * 100
        elif len(groups[0]) == 1 and groups[0][0] in ["百", "佰"]:
            result += 100
        else:
            return -1
    if groups[1]:  # 十位数字
        if len(groups[1]) == 2:
            result += digit_map[groups[1][0]] * 10
        elif len(groups[1]) == 1 and groups[1][0] in ["十", "拾"]:
            result += 10
        else:
            return -1
    if groups[2]:
        if len(groups[2]) == 2:
            result += digit_map[groups[2][1]]
        elif len(groups[2]) == 1 and groups[2][0] in digit_map.keys() and not groups[0] and not groups[1]:
            result += digit_map[groups[2][0]]
        else:
            return -1
    return result

def number_to_int_batch(texts: tuple):
    batched_tuple = [number_to_int(text) for text in texts]
    if any(num == -1 for num in batched_tuple):
        raise ValueError(f"不合法的数字：{texts[next(i for i, num in enumerate(batched_tuple) if num == -1)]}")
    batched_tuple = tuple(batched_tuple)
    return batched_tuple

def int_to_code(num: int):
    """
    将整数转换为编号
    """
    if num < len(odd_in_code) * len(even_in_code):
        return odd_in_code[num // len(even_in_code)] + even_in_code[num % len(even_in_code)]
    else:
        raise ValueError(f"整数 {num} 超出了编号范围")

def code_to_int(code: str):
    """
    将编号转换为整数
    """
    if len(code) == 2 and code[0] in odd_in_code and code[1] in even_in_code:
        return odd_in_code.index(code[0]) * len(even_in_code) + even_in_code.index(code[1])
    else:
        raise ValueError(f"不合法的编号 {code}")

def try_code_to_int_batch(codes: tuple):
    try:
        for code in codes:
            code_to_int(code)
    except ValueError as e:
        return str(e)
    return ""