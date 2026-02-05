import re
from structure import Structure
from numbering import all_in_number, all_in_code, number_to_int, int_to_code, code_to_int, try_code_to_int_batch, number_to_int_batch

help_str = """每指令一行。全角句号自动忽略。

添加构件: 
置柱于地横<数>寸纵<数>寸高<数>寸径<数>寸
置梁于柱<码>至柱<码>宽<数>寸高<数>寸内延<数>寸外延<数>寸
置柱于梁<码>深<数>寸高<数>寸径<数>寸
置枋于柱<码>至柱<码>起<数>寸宽<数>寸高<数>寸延<数>寸
置檩于柱<码>至柱<码>径<数>寸延<数>寸
置角梁于柱<码>至柱<码>宽<数>寸高<数>寸
置边椽于檩<码>(内|外)至檩<码>(内|外)
置斗拱于梁<码>深<数>寸(顺|逆)内横<数>寸纵<数>寸升<数>寸外横<数>寸纵<数>寸升<数>寸
置檩于斗拱<码>(内|外)至斗拱<码>(内|外)径<数>寸延<数>寸
置角梁于斗拱<码>宽<数>寸高<数>寸
置角梁于柱<码>至斗拱<码>(内|外)宽<数>寸高<数>寸
置封檐于斗拱<码>(内|外)至斗拱<码>(内|外)宽<数>寸高<数>寸

退出程序: Ctrl + C

显示本帮助
释"""

def parse_one_line(structure: Structure, line: str) -> tuple[bool, str]:
    line = re.sub(r'\s+', '', line)
    line = re.sub(r'。', '', line)
    # print(f"输入：{line}")

    re_dict = {
        "置柱于地": (r"置柱于地横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸径([" + all_in_number + r"]+)寸", ),
        "置梁于柱": (r"置梁于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)宽([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸内延([" + all_in_number + r"]+)寸外延([" + all_in_number + r"]+)寸", ),
        "置柱于梁": (r"置柱于梁([" + all_in_code + r"]+)深([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸径([" + all_in_number + r"]+)寸", ),
        "置枋于柱": (r"置枋于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)起([" + all_in_number + r"]+)寸宽([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸延([" + all_in_number + r"]+)寸", ),
        "置檩于柱": (r"置檩于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)径([" + all_in_number + r"]+)寸延([" + all_in_number + r"]+)寸", ),
        "置角梁于柱": (r"置角梁于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)宽([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置边椽于檩": (r"置边椽于檩([" + all_in_code + r"]+)(内|外)至檩([" + all_in_code + r"]+)(内|外)", ),
        "置斗拱于梁": (r"置斗拱于梁([" + all_in_code + r"]+)深([" + all_in_number + r"]+)寸(顺|逆)内横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸升([" + all_in_number + r"]+)寸外横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸升([" + all_in_number + r"]+)寸", ),
        "置檩于斗拱": (r"置檩于斗拱([" + all_in_code + r"]+)(内|外)至斗拱([" + all_in_code + r"]+)(内|外)径([" + all_in_number + r"]+)寸延([" + all_in_number + r"]+)寸",),
        "置角梁于斗拱": (r"置角梁于斗拱([" + all_in_code + r"]+)宽([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸",),
        "置角梁于柱至斗拱": (r"置角梁于柱([" + all_in_code + r"]+)至斗拱([" + all_in_code + r"]+)(内|外)宽([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸",),
        "置封檐于斗拱": (r"置封檐于斗拱([" + all_in_code + r"]+)(内|外)至斗拱([" + all_in_code + r"]+)(内|外)宽([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸",),
        "示形": (r"示形", ),
        "显轴": (r"显轴", ),
        "释": (r"释", ), 
    }

    re_str = re_dict["释"][0]
    match = re.match(re_str, line)
    if match:
        return True, help_str

    re_str = re_dict["示形"][0]
    match = re.match(re_str, line)
    if match:
        structure.render()
        return True, "显示成功"
    
    re_str = re_dict["显轴"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_ref = not structure.show_ref
        return True, "设置成功"
    
    re_str = re_dict["置柱于地"][0]
    match = re.match(re_str, line)
    if match:
        x, y, height, radius = match.groups()
        try:
            x, y, height, radius = number_to_int_batch((x, y, height, radius))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_zhu_on_di(line, x, y, height, radius)
            return True, f"置柱{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置梁于柱"][0]
    match = re.match(re_str, line)
    if match:
        zhu1, zhu2, width, height, in_ext, out_ext = match.groups()
        try_code_result = try_code_to_int_batch((zhu1, zhu2))
        if try_code_result != "":
            return False, try_code_result
        try:
            width, height, in_ext, out_ext = number_to_int_batch((width, height, in_ext, out_ext))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_liang_on_zhu(line, zhu1, zhu2, width, height, in_ext, out_ext)
            return True, f"置梁{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置柱于梁"][0]
    match = re.match(re_str, line)
    if match:
        liang1, depth, height, radius = match.groups()
        try_code_result = try_code_to_int_batch((liang1,))
        if try_code_result != "":
            return False, try_code_result
        try:
            depth, height, radius = number_to_int_batch((depth, height, radius))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_zhu_on_liang(line, liang1, depth, height, radius)
            return True, f"置柱{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置枋于柱"][0]
    match = re.match(re_str, line)
    if match:
        zhu1, zhu2, z, width, height, extend = match.groups()
        try_code_result = try_code_to_int_batch((zhu1, zhu2))
        if try_code_result != "":
            return False, try_code_result
        try:
            z, width, height, extend = number_to_int_batch((z, width, height, extend))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_fang_on_zhu(line, zhu1, zhu2, z, width, height, extend)
            return True, f"置枋{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置檩于柱"][0]
    match = re.match(re_str, line)
    if match:
        zhu1, zhu2, radius, extend = match.groups()
        try_code_result = try_code_to_int_batch((zhu1, zhu2))
        if try_code_result != "":
            return False, try_code_result
        try:
            radius, extend = number_to_int_batch((radius, extend))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_lin_on_zhu(line, zhu1, zhu2, radius, extend)
            return True, f"置檩{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置角梁于柱"][0]
    match = re.match(re_str, line)
    if match:
        zhu1, zhu2, width, height = match.groups()
        try_code_result = try_code_to_int_batch((zhu1, zhu2))
        if try_code_result != "":
            return False, try_code_result
        try:
            width, height = number_to_int_batch((width, height))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_jiaoliang_on_zhu(line, zhu1, zhu2, width, height)
            return True, f"置角梁{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置边椽于檩"][0]
    match = re.match(re_str, line)
    if match:
        lin1, in_or_out_1, lin2, in_or_out_2= match.groups()
        try_code_result = try_code_to_int_batch((lin1, lin2))
        if try_code_result != "":
            return False, try_code_result
        flag_1 = True if in_or_out_1 == "内" else False
        flag_2 = True if in_or_out_2 == "内" else False
        # 合法指令
        try:
            code = structure.add_bianchuan_on_lin(line, lin1, lin2, flag_1, flag_2)
            return True, f"置边椽{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置斗拱于梁"][0]
    match = re.match(re_str, line)
    if match:
        liang1, depth, pos, dx1, dy1, dz1, dx2, dy2, dz2 = match.groups()
        try_code_result = try_code_to_int_batch((liang1,))
        if try_code_result != "":
            return False, try_code_result
        try:
            depth, dx1, dy1, dz1, dx2, dy2, dz2 = number_to_int_batch((depth, dx1, dy1, dz1, dx2, dy2, dz2))
        except ValueError as e:
            return False, str(e)
        if pos == "顺":
            dx1, dy1 = -dx1, -dy1
        else:
            dx2, dy1 = -dx2, -dy1
        # 合法指令
        try:
            code = structure.add_dougong_on_liang(line, liang1, depth, dx1, dy1, dz1, dx2, dy2, dz2)
            return True, f"置斗拱{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置檩于斗拱"][0]
    match = re.match(re_str, line)
    if match:
        dougong1, pos1, dougong2, pos2, radius, extend = match.groups()
        try_code_result = try_code_to_int_batch((dougong1, dougong2))
        if try_code_result != "":
            return False, try_code_result
        try:
            radius, extend = number_to_int_batch((radius, extend))
        except ValueError as e:
            return False, str(e)
        side1 = 1 if pos1 == "内" else 2
        side2 = 1 if pos2 == "内" else 2
        # 合法指令
        try:
            code = structure.add_lin_on_dougong(line, dougong1, side1, dougong2, side2, radius, extend)
            return True, f"置檩{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置角梁于斗拱"][0]
    match = re.match(re_str, line)
    if match:
        dougong1, width, height = match.groups()
        try_code_result = try_code_to_int_batch((dougong1, ))
        if try_code_result != "":
            return False, try_code_result
        try:
            width, height = number_to_int_batch((width, height))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_jiaoliang_on_dougong(line, dougong1, width, height)
            return True, f"置角梁{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置角梁于柱至斗拱"][0]
    match = re.match(re_str, line)
    if match:
        jiaoliang1, dougong1, pos1, width, height = match.groups()
        try_code_result = try_code_to_int_batch((jiaoliang1, dougong1, ))
        if try_code_result != "":
            return False, try_code_result
        try:
            width, height = number_to_int_batch((width, height))
        except ValueError as e:
            return False, str(e)
        side1 = 1 if pos1 == "内" else 2
        # 合法指令
        try:
            code = structure.add_jiaoliang_out_zhu_to_dougong(line, jiaoliang1, dougong1, side1, width, height)
            return True, f"置角梁{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置封檐于斗拱"][0]
    match = re.match(re_str, line)
    if match:
        dougong1, pos1, dougong2, pos2, width, height = match.groups()
        try_code_result = try_code_to_int_batch((dougong1, dougong2))
        if try_code_result != "":
            return False, try_code_result
        try:
            width, height = number_to_int_batch((width, height))
        except ValueError as e:
            return False, str(e)
        side1 = 1 if pos1 == "内" else 2
        side2 = 1 if pos2 == "内" else 2
        # 合法指令
        try:
            code = structure.add_fengyan_on_dougong(line, dougong1, side1, dougong2, side2, width, height)
            return True, f"置封檐{code}"
        except ValueError as e:
            return False, str(e)

    for inst in re_dict.keys():
        if inst in line:
            return False, f"{inst} 是有效指令，但缺少参数"

    return False, "未匹配到指令"

# if __name__ == "__main__":
#     # 测试
#     test_cases = [
#         ("五百六十",560),
#         ("一百又五",105),
#         ("一百五十", 150),
#         ("二十有五",25),
#         ("五十",50),
#         ("百二十", 120),
#         ("十",10),
#         ("一百零五",-1),
#         ("四百二十又三等",-1),
#         ("三百二十五",-1),
#         ("一百五",-1),
#         ("四百二又三",-1),
#         ("二十一",-1),
#         ("二十一又三",-1),
#         ("一百零二",-1),
#         ("四百零二又三",-1)
#     ]
#     for case in test_cases:
#         res = number_to_int(case[0])
#         if res != case[1]:
#             print(f"{case[0]} -> {res} (期望: {case[1]})")
#     for case in [4, 12, 37]:
#         res = int_to_code(case)
#         print(f"{case} -> {res}")
#     for case in ["甲子", "乙丑", "丙寅", "丁卯"]:
#         res = code_to_int(case)
#         print(f"{case} -> {res}")
