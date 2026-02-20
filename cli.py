from parser import parse_one_line
from structure import Structure
import sys
import os

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
            line = input("> ")
            success, result = parse_one_line(structure, line)
            if success:
                structure.insts.append(line)
                structure.dump_insts()
                structure.render()
            print(result)
    elif len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        structure = Structure(sys.argv[1])
        for inst in structure.insts:
            if len(inst.strip()) == 0:
                continue
            _, result = parse_one_line(structure, inst)
            print(f"{result} <- {inst}")
        # print(len(structure.insts))
        structure.render()
