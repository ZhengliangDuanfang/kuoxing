from pywebio import start_server
from pywebio.input import input
from pywebio.output import put_column, put_row, put_scope, put_image, put_markdown, toast, use_scope, put_buttons, clear, popup
from pywebio.session import set_env
from pywebio.pin import pin, put_input, pin_update, put_textarea
from app.structure import Structure
from app.parser import parse_one_line, help_str
import os
import re
import sys
from functools import partial

basic_module_size = 600

def main(file_name: str):
    """主函数"""
    # 设置页面标题和布局
    set_env(title="廓形 - 图形化界面", output_animation=True)
    structure = Structure(file_name)
    for i, (inst, comment) in enumerate(zip(structure.insts, structure.comments)):
        if re.match(r'释', inst) or re.match(r'观处', inst) or re.match(r'审', inst):
            continue
        if len(inst.strip()) == 0:
            continue
        suc, result = parse_one_line(structure, inst)
        if not suc:
            toast(f"{result} <- {inst}", duration=5, color="error")
            continue
        if comment == "" and result != "设置成功":
            structure.comments[i] = result
    structure.render()
    structure.dump_insts()
    # 创建布局
    put_row([
        put_column([
            put_scope('img_display'),
            None,
            put_row([
                put_input('new_input', placeholder="追加执行指令。如需帮助。输入「释」。",),
                None,
                put_buttons(['执行',], onclick=[lambda: process_input(structure),]),
            ], size="1fr 10px auto"),
        ], size=f"{basic_module_size}px 10px 40px"),
        None,
        put_column([
            put_textarea('inst_display', value=structure.get_insts_and_comments(), rows=30,),
        ], size=f"{basic_module_size}px 10px 40px"),        
    ], size=f"{basic_module_size}px 10px {basic_module_size}px")

    if len(structure.insts) > 0:
        img = open(structure.save_path.split(".")[0] + ".png", 'rb').read()
        with use_scope('img_display', clear=False):
            put_image(img, height=f"{basic_module_size}px")
    else:
        with use_scope('img_display', clear=False):
            put_markdown("尚未生成图片预览")

def process_input(structure: Structure):
    input_data = str(pin['new_input'])
    insts_and_comments = str(pin['inst_display'])
    if insts_and_comments != structure.get_insts_and_comments():
        structure.clear_setting()
        for line in insts_and_comments.split("\n"):
            pos = line.find("#")
            if pos == -1:
                structure.comments.append("")
                inst = line.strip()
            else:
                comment = line[pos+1:].strip()
                if len(comment) == 4 and comment[0] == "置":
                    comment = ""
                structure.comments.append(comment)
                inst = line[:pos].strip()
            structure.insts.append(inst)
        for i, (inst, comment) in enumerate(zip(structure.insts, structure.comments)):
            if re.match(r'释', inst) or re.match(r'观处', inst) or re.match(r'审', inst):
                continue
            if len(inst.strip()) == 0:
                continue
            suc, result = parse_one_line(structure, inst)
            if not suc:
                toast(f"{result} <- {inst}", duration=5, color="error")
                continue
            if comment == "" and result != "设置成功":
                structure.comments[i] = result
    elif not input_data.strip():
        toast("未修改指令或输入新指令", duration=5, color='error')
        return
    if not input_data.strip():
        structure.render()
        pin_update('new_input', value='')
        pin_update('inst_display', value=structure.get_insts_and_comments())
        img = open(structure.save_path.split(".")[0] + ".png", 'rb').read()
        clear('img_display')
        with use_scope('img_display', clear=False):
            put_image(img, height=f"{basic_module_size}px")
        structure.dump_insts()
        return
    line = re.sub(r'\s+', '', input_data)
    line = re.sub(r'。', '', line)
    if re.match(r'释', line):
        pin_update('new_input', value='')
        popup('释', [
            put_markdown(help_str),
        ])
        return
    if re.match(r'观处', line):
        pin_update('new_input', value='')
        toast(f"观于径{structure.view_pos[0]}寸俯{structure.view_pos[1]}度侧{structure.view_pos[2]}度", duration=5, color="success")
        return
    if re.match(r'审', line):
        warning_list = structure.dependency_check()
        pin_update('new_input', value='')
        if len(warning_list) == 0:
            toast("未发现未使用构件", duration=5, color="success")
        else:
            toast("\n".join(warning_list), duration=5, color="error")
        return
    try:
        suc, result = parse_one_line(structure, input_data)
        if suc:
            toast(f"{result} <- {input_data}", duration=5, color="success")
            structure.insts.append(input_data)
            structure.comments.append(result if result != "设置成功" else "")
        else:
            toast(f"{result} <- {input_data}", duration=5, color="error")
            return
        structure.render()
        pin_update('new_input', value='')
        pin_update('inst_display', value=structure.get_insts_and_comments())
        img = open(structure.save_path.split(".")[0] + ".png", 'rb').read()
        clear('img_display')
        with use_scope('img_display', clear=False):
            put_image(img, height=f"{basic_module_size}px")
        structure.dump_insts()
    except Exception as e:
        toast(f"处理出错: {str(e)}", color='error')

if __name__ == '__main__':
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".txt"):
        print("Usage: python main.py <filename>.txt [port]")
        exit(1)
    file_name = str(sys.argv[1])
    port = int(sys.argv[2]) if len(sys.argv) == 3 else 8080
    
    if not os.path.isfile(file_name):
        try:
            with open(file_name, "w") as f:
                pass
            if not os.path.isfile(file_name):
                print(f"创建文件失败: {file_name}")
                exit(1)
        except:
            print(f"创建文件失败: {file_name}")
            exit(1)

    start_server(partial(main, file_name), host="localhost", port=port, debug=True, cdn=False, auto_open_webbrowser=True)