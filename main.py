from pywebio import start_server
from pywebio.input import input
from pywebio.output import put_column, put_row, put_scope, put_image, put_markdown, toast, use_scope, put_buttons, clear, popup
from pywebio.session import set_env
from pywebio.pin import pin, put_input, pin_update
from structure import Structure
from parser import parse_one_line, help_str
import os
import re
import sys
import webbrowser

def main():
    """主函数"""
    # 设置页面标题和布局
    set_env(title="实时输入输出界面", output_animation=False)
    while True:
        file_name = str(input("打开或创建文件"))
        if os.path.isfile(file_name):
            # toast(f"文件已存在: {file_name}")
            break
        try:
            with open(file_name, "w") as f:
                pass
            if os.path.isfile(file_name):
                break
        except:
            toast(f"创建文件失败: {file_name}", color="error")
    structure = Structure(file_name)
    for i, (inst, comment) in enumerate(zip(structure.insts, structure.comments)):
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
    put_column([
        put_scope('img_display'),
        put_row([
            put_input('new_input', placeholder="此处输入指令。如需帮助。输入「释」。",),
            put_buttons(['执行',], onclick=[lambda: process_input(structure),]),
        ], size="1fr auto"),
    ], size="720px 40px")

    if len(structure.insts) > 0:
        img = open(structure.save_path.split(".")[0] + ".png", 'rb').read()
        with use_scope('img_display', clear=False):
            put_image(img, height="720px")
    else:
        with use_scope('img_display', clear=False):
            put_markdown("尚未生成图片预览")

def process_input(structure: Structure):
    input_data = str(pin['new_input'])
    
    if not input_data.strip():
        toast("未有有效内容", duration=5, color='error')
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
        img = open(structure.save_path.split(".")[0] + ".png", 'rb').read()
        clear('img_display')
        with use_scope('img_display', clear=False):
            put_image(img, height="720px")
        structure.dump_insts()
    except Exception as e:
        toast(f"处理出错: {str(e)}", color='error')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8080
    # 打开默认浏览器
    webbrowser.open(f"http://localhost:{port}")
    start_server(main, port=port, debug=True, cdn=False)