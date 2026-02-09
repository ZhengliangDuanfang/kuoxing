import re
from structure import Structure
from numbering import all_in_number, all_in_code, number_to_int, int_to_code, code_to_int, try_code_to_int_batch, number_to_int_batch

help_str = """每指令一行。全角句号自动忽略。

添加构件: 
置柱于地横<数>寸纵<数>寸高<数>寸
置柱于梁<码>深<数>寸高<数>寸
置柱于栱<码>(内|外)高<数>寸
置梁于柱<码>至柱<码>内延<数>寸外延<数>寸
置栱于梁<码>深<数>寸(顺|逆)内横<数>寸纵<数>寸高<数>寸外横<数>寸纵<数>寸高<数>寸
置枋于柱<码>至柱<码>起<数>寸宽<数>寸高<数>寸内延<数>寸外延<数>寸
置檩于柱<码>至柱<码>延<数>寸
置檩于栱<码>(内|外)至栱<码>(内|外)延<数>寸
置槽于柱<码>
置槽于栱<码>(内|外)
置脊于檩<码>(内|外)至檩<码>(内|外)
置脊于槽<码>至槽<码>
置檐于脊<码>至脊<码>

调整视角:
观于径<数>寸俯<数>度侧<数>度

退出程序: Ctrl + C

显示本帮助: 
释"""

def parse_one_line(structure: Structure, line: str) -> tuple[bool, str]:
    line = re.sub(r'\s+', '', line)
    line = re.sub(r'。', '', line)
    # print(f"输入：{line}")

    re_dict = {
        "置柱于地": (r"置柱于地横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置柱于梁一": (r"置柱于梁([" + all_in_code + r"]+)深([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置柱于栱一": (r"置柱于栱(内|外)([" + all_in_code + r"]+)高([" + all_in_number + r"]+)寸", ),
        "置梁于柱二": (r"置梁于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)内延([" + all_in_number + r"]+)寸外延([" + all_in_number + r"]+)寸", ),
        "置栱于梁一": (r"置栱于梁([" + all_in_code + r"]+)深([" + all_in_number + r"]+)寸(顺|逆)内横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸外横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置枋于柱二": (r"置枋于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)起([" + all_in_number + r"]+)寸内延([" + all_in_number + r"]+)寸外延([" + all_in_number + r"]+)寸", ),

        "置檩于柱二": (r"置檩于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)延([" + all_in_number + r"]+)寸", ),
        "置檩于栱二": (r"置檩于栱([" + all_in_code + r"]+)(内|外)至栱([" + all_in_code + r"]+)(内|外)延([" + all_in_number + r"]+)寸",),
        
        "置槽于柱一": (r"置槽于柱([" + all_in_code + r"]+)", ),
        "置槽于栱一": (r"置槽于栱([" + all_in_code + r"]+)(内|外)", ),
        "置脊于檩二": (r"置脊于檩([" + all_in_code + r"]+)(内|外)至檩([" + all_in_code + r"]+)(内|外)", ),
        "置脊于槽二": (r"置脊于槽([" + all_in_code + r"]+)至槽([" + all_in_code + r"]+)", ),
        "置檐于脊二": (r"置檐于脊([" + all_in_code + r"]+)至脊([" + all_in_code + r"]+)", ),
        
        "示形": (r"示形", ),
        "显轴": (r"显轴", ),
        "释": (r"释", ), 
        "观": (r"观于径([" + all_in_number + r"]+)寸俯([" + all_in_number + r"]+)度侧([" + all_in_number + r"]+)度", ),
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
    
    re_str = re_dict["观"][0]
    match = re.match(re_str, line)
    if match:
        r, phi, theta = match.groups()
        try:
            r, phi, theta = number_to_int_batch((r, phi, theta))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        structure.view_pos = [r, phi, theta]
        return True, "设置成功"
    
    re_str = re_dict["置柱于地"][0]
    match = re.match(re_str, line)
    if match:
        x, y, height = match.groups()
        try:
            x, y, height = number_to_int_batch((x, y, height))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_zhu_on_di(x, y, height)
            return True, f"置柱{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置柱于梁一"][0]
    match = re.match(re_str, line)
    if match:
        liang1, depth, height = match.groups()
        try_code_result = try_code_to_int_batch((liang1,))
        if try_code_result != "":
            return False, try_code_result
        try:
            depth, height = number_to_int_batch((depth, height))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_zhu_on_liang_1(liang1, depth, height)
            return True, f"置柱{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置柱于栱一"][0]
    match = re.match(re_str, line)
    if match:
        in_or_out1, gong1, height = match.groups()
        try_code_result = try_code_to_int_batch((gong1,))
        if try_code_result != "":
            return False, try_code_result
        try:
            height = number_to_int_batch((height,))[0]
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_zhu_on_gong_1(gong1, in_or_out1, height)
            return True, f"置柱{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置梁于柱二"][0]
    match = re.match(re_str, line)
    if match:
        zhu1, zhu2, in_ext, out_ext = match.groups()
        try_code_result = try_code_to_int_batch((zhu1, zhu2))
        if try_code_result != "":
            return False, try_code_result
        try:
            in_ext, out_ext = number_to_int_batch((in_ext, out_ext))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_liang_on_zhu_2(zhu1, zhu2, in_ext, out_ext)
            return True, f"置梁{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置栱于梁一"][0]
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
        # 合法指令
        try:
            code = structure.add_gong_on_liang_1(liang1, depth, pos, dx1, dy1, dz1, dx2, dy2, dz2)
            return True, f"置栱{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置枋于柱二"][0]
    match = re.match(re_str, line)
    if match:
        zhu1, zhu2, dz, in_ext, out_ext = match.groups()
        try_code_result = try_code_to_int_batch((zhu1, zhu2))
        if try_code_result != "":
            return False, try_code_result
        try:
            dz, in_ext, out_ext = number_to_int_batch((dz, in_ext, out_ext))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_fang_on_zhu_2(zhu1, zhu2, dz, in_ext, out_ext)
            return True, f"置枋{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置檩于柱二"][0]
    match = re.match(re_str, line)
    if match:
        zhu1, zhu2, extend = match.groups()
        try_code_result = try_code_to_int_batch((zhu1, zhu2))
        if try_code_result != "":
            return False, try_code_result
        try:
            extend = number_to_int_batch((extend,))[0]
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_lin_on_zhu_2(zhu1, zhu2, extend)
            return True, f"置檩{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置檩于栱二"][0]
    match = re.match(re_str, line)
    if match:
        gong1, in_or_out1, gong2, in_or_out2, extend = match.groups()
        try_code_result = try_code_to_int_batch((gong1, gong2))
        if try_code_result != "":
            return False, try_code_result
        try:
            extend = number_to_int_batch((extend,))[0]
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_lin_on_gong_2(gong1, in_or_out1, gong2, in_or_out2, extend)
            return True, f"置檩{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置槽于柱一"][0]
    match = re.match(re_str, line)
    if match:
        zhu1 = match.groups()[0]
        try_code_result = try_code_to_int_batch((zhu1,))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_cao_on_zhu_1(zhu1)
            return True, f"置槽{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置槽于栱一"][0]
    match = re.match(re_str, line)
    if match:
        gong1, in_or_out1 = match.groups()
        try_code_result = try_code_to_int_batch((gong1,))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_cao_on_gong_1(gong1, in_or_out1)
            return True, f"置槽{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置脊于檩二"][0]
    match = re.match(re_str, line)
    if match:
        lin1, in_or_out1, lin2, in_or_out2 = match.groups()
        try_code_result = try_code_to_int_batch((lin1, lin2))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_ji_on_lin_2(lin1, in_or_out1, lin2, in_or_out2)
            return True, f"置脊{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置脊于槽二"][0]
    match = re.match(re_str, line)
    if match:
        cao1, cao2 = match.groups()
        try_code_result = try_code_to_int_batch((cao1, cao2))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_ji_on_cao_2(cao1, cao2)
            return True, f"置脊{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置檐于脊二"][0]
    match = re.match(re_str, line)
    if match:
        ji1, ji2 = match.groups()
        try_code_result = try_code_to_int_batch((ji1, ji2))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_yan_on_ji_2(ji1, ji2)
            return True, f"置檐{code}"
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
