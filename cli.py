from parser import parse_one_line, help_str
from structure import Structure
import sys
import os
import re

if __name__ == "__main__":
    if len(sys.argv) == 1:
        while True:
            save_path = input("保存为: ")
            try:
                with open(save_path, "w") as f:
                    pass
                if os.path.isfile(save_path):
                    break
            except:
                print(f"创建文件失败: {save_path}")
        structure = Structure(save_path)
        while True:
            input_data = input("> ")
            line = re.sub(r'\s+', '', input_data)
            line = re.sub(r'。', '', line)
            if re.match(r'释', line):
                print(help_str)
                continue
            if re.match(r'观处', line):
                print(f"观于径{structure.view_pos[0]}寸俯{structure.view_pos[1]}度侧{structure.view_pos[2]}度")
                continue
            if re.match(r'审', line):
                warning_list = structure.dependency_check()
                if len(warning_list) == 0:
                    print("未发现未使用构件")
                else:
                    print("\n".join(warning_list))
                continue
            success, result = parse_one_line(structure, input_data)
            if success:
                structure.insts.append(input_data)
                structure.comments.append(result if result != "设置成功" else "")
                structure.render()
                structure.dump_insts()
            print(result)
    elif len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            print(f"文件不存在: {sys.argv[1]}")
            exit(1)
        structure = Structure(sys.argv[1])
        for inst, comment in zip(structure.insts, structure.comments):
            if len(inst.strip()) == 0:
                continue
            _, result = parse_one_line(structure, inst)
            if comment == "" and result != "设置成功":
                comment = result
            print(f"{result} <- {inst}")
        # print(len(structure.insts))
        structure.render()
        structure.dump_insts()
