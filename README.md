# 形制

木构建筑搭建模拟

```shell
# 搭建环境
python -m venv venv
source venv/Scripts/activate # Git Bash
pip install -r requirements.txt

# 新建文件
python main.py
# 运行脚本
python main.py test/yingshanding.txt

```

脚本执行语义规则：

```
# 显示提示
释
# 添加构件示例
置梁于柱甲寅至柱甲卯。宽八寸。高十寸。内延二十寸。外延五十寸。
```

## 路线图

[ ] 构件
    [x] 柱
    [x] 檩
    [x] 梁
    [x] 枋
    [x] 角梁
    [x] 边椽
    [x] 斗拱
    [ ] 封檐
    [ ] 覆瓦
    [ ] 墙
[ ] 规则
    [ ] 检查规则
        [ ] 重合构件
[ ] 显示
    [ ] 桌面显示界面
    [ ] 视角调整
    [ ] 组件设色