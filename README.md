# 廓形

使用极少种类的构件模拟中国传统木构建筑的大致轮廓。使用单行命令的交互操作构件。

注：本项目中的构件名称与中国传统木构建筑中的构件名称并不重合，搭建的具体依赖规则也有所差异。本项目仅尝试给出一种模拟的方法，对于中国传统木构建筑的实际情况，请参考其它资料。

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
# 显示帮助
释
# 添加构件示例
置梁于柱甲寅至柱甲卯。内延二十寸。外延五十寸。
```

## 路线图

[ ] 构件
    [x] 柱
    [x] 梁
    [x] 栱
    [x] 枋
    [x] 檩
    [x] 槽
    [x] 脊
    [x] 檐
    [ ] 顶
    [ ] 墙
[ ] 规则
    [ ] 检查规则
        [ ] 重合构件
[ ] 显示
    [ ] 桌面显示界面
    [ ] 视角调整
    [ ] 组件设色