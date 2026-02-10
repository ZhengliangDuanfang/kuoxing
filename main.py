from pywebio import start_server
from pywebio.input import input
from pywebio.output import put_column, put_row, put_scope, put_image, put_markdown, toast, use_scope, put_buttons, clear, popup
from pywebio.session import set_env
from pywebio.pin import pin, put_input, pin_update
from structure import Structure
from parser import parse_one_line
import os
import re
from parser import help_str

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
    for inst in structure.insts:
        _, result = parse_one_line(structure, inst)
    structure.render()
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
    try:
        suc, result = parse_one_line(structure, input_data)
        if suc:
            toast(f"{result} <- {input_data}", duration=5, color="success")
            structure.insts.append(input_data)
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
    start_server(main, port=8080, debug=True)