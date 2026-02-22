import re
from app.structure import Structure
from app.numbering import all_in_number, all_in_code, part_map, color_map, try_code_to_int_batch, number_to_int_batch

help_str = """每指令一行。全角句号自动忽略。
```
# 添加构件
置柱于地横<数>寸纵<数>寸高<数>寸
置柱于梁<码>深<数>寸高<数>寸
置柱于栱<码>(内|外)高<数>寸
置垂花柱于梁<码>深<数>寸高<数>寸垂<数>寸
置梁于柱<码>至柱<码>内延<数>寸外延<数>寸
置栱于梁<码>深<数>寸(顺|逆)内横<数>寸纵<数>寸高<数>寸外横<数>寸纵<数>寸高<数>寸
置枋于柱<码>起<数>寸至柱<码>起<数>寸宽<数>寸高<数>寸内延<数>寸外延<数>寸
置檩于柱<码>至柱<码>延<数>寸
置檩于栱<码>(内|外)至栱<码>(内|外)延<数>寸
置点于柱<码>
置点于栱<码>(内|外)
置点于檩<码>(内|外)
置顶于点<码>至点<码>及点<码>
置顶于点<码>及点<码>至点<码>及点<码>
置脊于点<码>至点<码>
置四角墙于横<数>寸纵<数>寸高<数>寸至横<数>寸纵<数>寸高<数>寸
置三角墙于横<数>寸纵<数>寸高<数>寸至横<数>寸纵<数>寸高<数>寸
```
- `<码>`以天干地支形式，见于添加成功提示。
- `<数>`应以「一百二十有三」形式，接受从零到九百九十有九的范围。
- `<构>`表示构件类型（柱、梁、栱、枋、檩、点、顶、脊、墙）。
- `<色>`表示可选择的显示颜色（朱、橙、黄、绿、青、蓝、紫、黛、棕、黑）。
- `(甲|乙)`意为二选一即可。
- 「内」「外」以横纵坐标区分构件端侧。

```
起顶以<数>寸 # 使脊、顶在显示时，相比于设定位置，额外抬高一定高度
观处 # 获取当前视角
观于径<数>寸俯<数>度侧<数>度 # 调整视角
显轴/隐轴 # 显示/隐藏坐标轴
显顶边/隐顶边 # 显示/隐藏顶边
实面/虚面 # 不透明化/透明化
示<构>以<色> # 修改特定类型构件颜色
示<构><码>以<色> # 修改单个构件颜色
设构径<数>寸 # 设置全部构件线条显示宽度
审 # 检查未使用构件
释 # 显示本帮助
```
在批量执行时，指令`释`、`审`以及`观处`不会被执行。"""

def parse_one_line(structure: Structure, line: str) -> tuple[bool, str]:
    line = re.sub(r'\s+', '', line)
    line = re.sub(r'。', '', line)
    # print(f"输入：{line}")

    re_dict = {
        # 基础结构
        "置柱于地": (r"置柱于地横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置柱于梁一": (r"置柱于梁([" + all_in_code + r"]+)深([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置柱于栱一": (r"置柱于栱(内|外)([" + all_in_code + r"]+)高([" + all_in_number + r"]+)寸", ),
        "置梁于柱二": (r"置梁于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)内延([" + all_in_number + r"]+)寸外延([" + all_in_number + r"]+)寸", ),
        "置栱于梁一": (r"置栱于梁([" + all_in_code + r"]+)深([" + all_in_number + r"]+)寸(顺|逆)内横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸外横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置枋于柱二": (r"置枋于柱([" + all_in_code + r"]+)起([" + all_in_number + r"]+)寸至柱([" + all_in_code + r"]+)起([" + all_in_number + r"]+)寸内延([" + all_in_number + r"]+)寸外延([" + all_in_number + r"]+)寸", ),
        "置垂花柱于梁一": (r"置垂花柱于梁([" + all_in_code + r"]+)深([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸垂([" + all_in_number + r"]+)寸", ),
        "置四角墙": (r"置四角墙于横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸至横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置三角墙": (r"置三角墙于横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸至横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        # 屋面结构
        "置檩于柱二": (r"置檩于柱([" + all_in_code + r"]+)至柱([" + all_in_code + r"]+)延([" + all_in_number + r"]+)寸", ),
        "置檩于栱二": (r"置檩于栱([" + all_in_code + r"]+)(内|外)至栱([" + all_in_code + r"]+)(内|外)延([" + all_in_number + r"]+)寸",),
        "置点于柱一": (r"置点于柱([" + all_in_code + r"]+)", ),
        "置点于栱一": (r"置点于栱([" + all_in_code + r"]+)(内|外)", ),
        "置点于檩一": (r"置点于檩([" + all_in_code + r"]+)(内|外)", ),
        "置点于空": (r"置点于横([" + all_in_number + r"]+)寸纵([" + all_in_number + r"]+)寸高([" + all_in_number + r"]+)寸", ),
        "置顶于点三": (r"置顶于点([" + all_in_code + r"]+)至点([" + all_in_code + r"]+)及点([" + all_in_code + r"]+)", ),
        "置顶于点四": (r"置顶于点([" + all_in_code + r"]+)及点([" + all_in_code + r"]+)至点([" + all_in_code + r"]+)及点([" + all_in_code + r"]+)", ),
        "置脊于点二": (r"置脊于点([" + all_in_code + r"]+)至点([" + all_in_code + r"]+)", ),
        "起顶": (r"起顶以([" + all_in_number + r"]+)寸", ),
        # 一般显示设置
        "显轴": (r"显轴", ),
        "隐轴": (r"隐轴", ),
        "观于": (r"观于径([" + all_in_number + r"]+)寸俯([" + all_in_number + r"]+)度侧([" + all_in_number + r"]+)度", ),
        "皆示": (r"示(["+ "".join(part_map.keys()) + r"])以(["+ "".join(color_map.keys()) + r"])", ),
        "示": (r"示(["+ "".join(part_map.keys()) + r"])([" + all_in_code + r"]+)以(["+ "".join(color_map.keys()) + r"])", ),
        "设构径": (r"设构径([" + all_in_number + r"]+)寸", ),
        # 渲染显示设置
        "显顶边": (r"显顶边", ),
        "隐顶边": (r"隐顶边", ),
        "实面": (r"实面", ),
        "虚面": (r"虚面", ),
        "显点": (r"显点", ),
        "隐点": (r"隐点", ),
    }

    re_str = re_dict["设构径"][0]
    match = re.match(re_str, line)
    if match:
        r = match.groups()[0]
        try:
            r = number_to_int_batch((r,))[0]
        except ValueError as e:
            return False, str(e)
        # 合法指令
        structure.linewidth = r
        return True, "设置成功"

    re_str = re_dict["显点"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_dian = True
        return True, "设置成功"

    re_str = re_dict["隐点"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_dian = False
        return True, "设置成功"

    re_str = re_dict["显顶边"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_ding_edge = True
        return True, "设置成功"

    re_str = re_dict["隐顶边"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_ding_edge = False
        return True, "设置成功"

    re_str = re_dict["实面"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_surface_transparent = False
        return True, "设置成功"

    re_str = re_dict["虚面"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_surface_transparent = True
        return True, "设置成功"

    re_str = re_dict["起顶"][0]
    match = re.match(re_str, line)
    if match:
        up = match.groups()[0]
        try:
            up = number_to_int_batch((up,))[0]
        except ValueError as e:
            return False, str(e)
        # 合法指令
        structure.ding_up = up
        return True, "设置成功"

    re_str = re_dict["示"][0]
    match = re.match(re_str, line)
    if match:
        part, code, color = match.groups()
        try_code_result = try_code_to_int_batch((code,))
        if try_code_result != "":
            return False, try_code_result
        if part not in part_map.keys():
            return False, f"未知构件类型{part}"
        if part == "点":
            structure.show_dian = True
        # 合法指令
        structure.set_color(part_map[part], code, color_map[color])
        return True, "设置成功"
    
    re_str = re_dict["皆示"][0]
    match = re.match(re_str, line)
    if match:
        part, color = match.groups()
        if part not in part_map.keys():
            return False, f"未知构件类型{part}"
        if part == "点":
            structure.show_dian = True
        # 合法指令
        structure.set_colors(part_map[part], color_map[color])
        return True, "设置成功"
    
    re_str = re_dict["显轴"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_ref = True
        return True, "设置成功"

    re_str = re_dict["隐轴"][0]
    match = re.match(re_str, line)
    if match:
        structure.show_ref = False
        return True, "设置成功"
    
    re_str = re_dict["观于"][0]
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
        zhu1, dz1, zhu2, dz2, in_ext, out_ext = match.groups()
        try_code_result = try_code_to_int_batch((zhu1, zhu2))
        if try_code_result != "":
            return False, try_code_result
        try:
            dz1, dz2, in_ext, out_ext = number_to_int_batch((dz1, dz2, in_ext, out_ext))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_fang_on_zhu_2(zhu1, zhu2, dz1, dz2, in_ext, out_ext)
            return True, f"置枋{code}"
        except ValueError as e:
            return False, str(e)
    
    re_str = re_dict["置垂花柱于梁一"][0]
    match = re.match(re_str, line)
    if match:
        liang1, deep, height, lower = match.groups()
        try_code_result = try_code_to_int_batch((liang1,))
        if try_code_result != "":
            return False, try_code_result
        try:
            deep, height, lower = number_to_int_batch((deep, height, lower))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_chui_on_liang_1(liang1, deep, height, lower)
            return True, f"置柱{code}"
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

    re_str = re_dict["置点于柱一"][0]
    match = re.match(re_str, line)
    if match:
        zhu1 = match.groups()[0]
        try_code_result = try_code_to_int_batch((zhu1,))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_dian_on_zhu_1(zhu1)
            return True, f"置点{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置点于栱一"][0]
    match = re.match(re_str, line)
    if match:
        gong1, in_or_out1 = match.groups()
        try_code_result = try_code_to_int_batch((gong1,))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_dian_on_gong_1(gong1, in_or_out1)
            return True, f"置点{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置点于檩一"][0]
    match = re.match(re_str, line)
    if match:
        lin1, in_or_out1 = match.groups()
        try_code_result = try_code_to_int_batch((lin1,))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_dian_on_lin_1(lin1, in_or_out1)
            return True, f"置点{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置点于空"][0]
    match = re.match(re_str, line)
    if match:
        x, y, z = match.groups()
        try:
            x, y, z = number_to_int_batch((x, y, z))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_dian_in_air(x, y, z)
            return True, f"置点{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置顶于点三"][0]
    match = re.match(re_str, line)
    if match:
        dian1, dian2, dian3 = match.groups()
        try_code_result = try_code_to_int_batch((dian1, dian2, dian3))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_ding_on_dian_3(dian1, dian2, dian3)
            return True, f"置顶{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置顶于点四"][0]
    match = re.match(re_str, line)
    if match:
        dian1, dian2, dian3, dian4 = match.groups()
        try_code_result = try_code_to_int_batch((dian1, dian2, dian3, dian4))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_ding_on_dian_4(dian1, dian2, dian3, dian4)
            return True, f"置顶{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置脊于点二"][0]
    match = re.match(re_str, line)
    if match:
        dian1, dian2 = match.groups()
        try_code_result = try_code_to_int_batch((dian1, dian2))
        if try_code_result != "":
            return False, try_code_result
        # 合法指令
        try:
            code = structure.add_ji_on_dian_2(dian1, dian2)
            return True, f"置脊{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置四角墙"][0]
    match = re.match(re_str, line)
    if match:
        x1, y1, z1, x2, y2, z2 = match.groups()
        try:
            x1, y1, z1, x2, y2, z2 = number_to_int_batch((x1, y1, z1, x2, y2, z2))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_rect_wall(x1, y1, z1, x2, y2, z2)
            return True, f"置墙{code}"
        except ValueError as e:
            return False, str(e)

    re_str = re_dict["置三角墙"][0]
    match = re.match(re_str, line)
    if match:
        x1, y1, z1, x2, y2, z2 = match.groups()
        try:
            x1, y1, z1, x2, y2, z2 = number_to_int_batch((x1, y1, z1, x2, y2, z2))
        except ValueError as e:
            return False, str(e)
        # 合法指令
        try:
            code = structure.add_tri_wall(x1, y1, z1, x2, y2, z2)
            return True, f"置墙{code}"
        except ValueError as e:
            return False, str(e)

    for inst in re_dict.keys():
        if inst in line:
            return False, f"{inst} 是有效指令，但缺少参数或格式错误"

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
