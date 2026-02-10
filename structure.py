from parts import Zhu, Liang, Gong, Lin, Fang, Cao, Ji, Yan
from numbering import int_to_code
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Structure:
    def __init__(self, save_path: str = "example.txt"):
        self.save_path = save_path
        self.parts = []
        self.insts = []
        self.zhu_int = 0
        self.liang_int = 0
        self.gong_int = 0
        self.lin_int = 0
        self.fang_int = 0
        self.cao_int = 0
        self.ji_int = 0
        self.yan_int = 0
        self.show_ref = False
        self.view_pos = [1000, 30, 30]

        with open(save_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and len(line) > 0:
                    self.insts.append(line)
        
        matplotlib.use('Agg')

    def render(self):
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        if not self.show_ref:
            self.ax.set_axis_off()
        lines = [p.endpoints() for p in self.parts if not isinstance(p, Gong) and not isinstance(p, Cao)]
        for p in self.parts: 
            if isinstance(p, Gong):
                lines += p.endpoint_list()

        for start, end in lines:
            points = np.array([start, end])
            self.ax.plot(points[:, 0], points[:, 1], points[:, 2], color='black', linewidth=3)

        self.ax.view_init(elev=self.view_pos[1], azim=self.view_pos[2])  
        max_range = self.view_pos[0]
        self.ax.set_xlim([0, max_range])
        self.ax.set_ylim([0, max_range])
        self.ax.set_zlim([0, max_range])
        
        # 保存图片
        plt.tight_layout()
        plt.savefig(f'{self.save_path.split(".")[0]}.png', dpi=300, bbox_inches='tight')

    def dump_insts(self):
        insts = "\n".join(self.insts)
        with open(self.save_path, "w", encoding="utf-8") as f:
            f.write(insts)

    def find_part(self, class_name: str, code: str):
        for part in self.parts:
            if isinstance(part, eval(class_name)) and part.code == code:
                return part
        return None

    def add_zhu_on_di(self, x: int, y: int, height: int):
        new_code = int_to_code(self.zhu_int)
        self.zhu_int += 1
        self.parts.append(Zhu(new_code, x, y, 0, height, [], []))
        return new_code

    def add_zhu_on_liang_1(self, liang: str, depth: int, height: int):
        founded_liang = self.find_part("Liang", liang)
        if founded_liang is None:
            raise ValueError(f"未有梁{liang}。")
        (x1, y1, z1), (x2, y2, z2) = founded_liang.endpoints()
        if x1 == x2:
            x = x1
            y = y1 + depth
        elif y1 == y2:
            y = y1
            x = x1 + depth
        else:
            raise ValueError("梁需并于横轴。或于纵轴。")

        new_code = int_to_code(self.zhu_int)
        self.zhu_int += 1
        self.parts.append(Zhu(new_code, x, y, z1, height, [liang], []))
        return new_code
    
    def add_zhu_on_gong_1(self, gong: str, in_or_out:str, height: int):
        founded_gong = self.find_part("Gong", gong)
        if founded_gong is None:
            raise ValueError(f"未有栱{gong}。")
        if in_or_out == "内":
            _, (x1, y1, z1) = founded_gong.endpoints()
        else:
            (x1, y1, z1), _ = founded_gong.endpoints()

        new_code = int_to_code(self.zhu_int)
        self.zhu_int += 1
        self.parts.append(Zhu(new_code, x1, y1, z1, height, [], [gong]))
        return new_code

    def add_liang_on_zhu_2(self, zhu1: str, zhu2: str, in_ext: int, out_ext: int):
        founded_zhus = []
        for zhu in [zhu1, zhu2]:
            founded_zhu = self.find_part("Zhu", zhu)
            if founded_zhu is None:
                raise ValueError(f"未有柱{zhu}。")
            founded_zhus.append(founded_zhu)
        x1, y1 = founded_zhus[0].x, founded_zhus[0].y
        x2, y2 = founded_zhus[1].x, founded_zhus[1].y
        base_zhus = [zhu1, zhu2]
        if x1 != x2 and y1 != y2:
            raise ValueError("梁需并于横轴。或于纵轴。")
        elif (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            y1, y2 = y2, y1
            x1, x2 = x2, x1
            base_zhus[0], base_zhus[1] = base_zhus[1], base_zhus[0]
        top_z_zhus = min([zhu.z + zhu.height for zhu in founded_zhus])

        new_code = int_to_code(self.liang_int)
        self.liang_int += 1
        self.parts.append(Liang(new_code, x1, x2, y1, y2, top_z_zhus, in_ext, out_ext, base_zhus))
        return new_code

    def add_gong_on_liang_1(self, liang: str, depth:int, pos: str, dx1:int, dy1:int, dz1:int, dx2:int, dy2:int, dz2:int):
        founded_liang = self.find_part("Liang", liang)
        if founded_liang is None:
            raise ValueError(f"未有梁{liang}。")
        (x1, y1, z1), (x2, y2, z2) = founded_liang.endpoints()
        if x1 == x2:
            y1 = y1 + depth
        elif y1 == y2:
            x1 = x1 + depth
        else:
            raise ValueError("梁需并于横轴。或于纵轴。")
        if pos == "顺":
            dx1, dy1 = -dx1, -dy1
        else:
            dx2, dy1 = -dx2, -dy1
        
        new_code = int_to_code(self.gong_int)
        self.gong_int += 1
        self.parts.append(Gong(new_code, x1, y1, z1, x1+dx1, y1+dy1, z1+dz1, x1+dx2, y1+dy2, z1+dz2, [founded_liang]))
        
        return new_code

    def add_fang_on_zhu_2(self, zhu1: str, zhu2: str, z: int, in_ext: int, out_ext: int):
        founded_zhus = []
        for zhu in [zhu1, zhu2]:
            founded_zhu = self.find_part("Zhu", zhu)
            if founded_zhu is None:
                raise ValueError(f"未有柱{zhu}。")
            founded_zhus.append(founded_zhu)
        x1, y1, z1, h1 = founded_zhus[0].x, founded_zhus[0].y, founded_zhus[0].z, founded_zhus[0].height
        x2, y2, z2, h2 = founded_zhus[1].x, founded_zhus[1].y, founded_zhus[1].z, founded_zhus[1].height
        base_zhus = [zhu1, zhu2]
        if z1 != z2:
            raise ValueError("柱其共枋者。底需同高。")
        if z > min(h1, h2):
            raise ValueError("枋不可高出二柱其一。")
        if x1 != x2 and y1 != y2:
            raise ValueError("枋需并于横轴。或于纵轴。")
        elif (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            y1, y2 = y2, y1
            x1, x2 = x2, x1
            base_zhus[0], base_zhus[1] = base_zhus[1], base_zhus[0]
        
        new_code = int_to_code(self.fang_int)
        self.fang_int += 1
        self.parts.append(Fang(new_code, x1, x2, y1, y2, z1+z, in_ext, out_ext, base_zhus))
        return new_code

    def add_lin_on_zhu_2(self, zhu1: str, zhu2: str, extend: int):
        founded_zhus = []
        for zhu in [zhu1, zhu2]:
            founded_zhu = self.find_part("Zhu", zhu)
            if founded_zhu is None:
                raise ValueError(f"未有柱{zhu}。")
            founded_zhus.append(founded_zhu)
        _, (x1, y1, z1) = founded_zhus[0].endpoints()
        _, (x2, y2, z2) = founded_zhus[1].endpoints()

        base_zhus = [zhu1, zhu2]
        if z1 != z2:
            raise ValueError("檩之始终需同高。故二柱之顶端需同高。")
        if x1 != x2 and y1 != y2:
            raise ValueError("檩需并于横轴。或于纵轴。")
        elif (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            y1, y2 = y2, y1
            x1, x2 = x2, x1
            base_zhus[0], base_zhus[1] = base_zhus[1], base_zhus[0]

        new_code = int_to_code(self.lin_int)
        self.lin_int += 1
        self.parts.append(Lin(new_code, x1, x2, y1, y2, z1, extend, base_zhus, []))
        return new_code

    def add_lin_on_gong_2(self, gong1: str, in_or_out1:str, gong2: str, in_or_out2:str, extend: int):
        founded_gongs = []
        for gong in [gong1, gong2]:
            founded_gong = self.find_part("Gong", gong)
            if founded_gong is None:
                raise ValueError(f"未有栱{gong}。")
            founded_gongs.append(founded_gong)
        if in_or_out1 == "内":
            x1, y1, z1 = founded_gongs[0].x1, founded_gongs[0].y1, founded_gongs[0].z1
        else:
            x1, y1, z1 = founded_gongs[0].x2, founded_gongs[0].y2, founded_gongs[0].z2
        if in_or_out2 == "内":
            x2, y2, z2 = founded_gongs[1].x1, founded_gongs[1].y1, founded_gongs[1].z1
        else:
            x2, y2, z2 = founded_gongs[1].x2, founded_gongs[1].y2, founded_gongs[1].z2

        base_gongs = [gong1, gong2]
        if z1 != z2:
            raise ValueError("檩之始终需同高。故二栱之顶端需同高。")
        if x1 != x2 and y1 != y2:
            raise ValueError("檩需并于横轴。或于纵轴。")
        elif (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            x1, y1, z1 = x2, y2, z2
            x2, y2, z2 = x1, y1, z1
            base_gongs[0], base_gongs[1] = base_gongs[1], base_gongs[0]
        
        new_code = int_to_code(self.lin_int)
        self.lin_int += 1
        self.parts.append(Lin(new_code, x1, x2, y1, y2, z1, extend, [], base_gongs))
        return new_code

    def add_cao_on_zhu_1(self, zhu: str):
        founded_zhu = self.find_part("Zhu", zhu)
        if founded_zhu is None:
            raise ValueError(f"未有柱{zhu}。")
        _, (x, y, z) = founded_zhu.endpoints()
        
        new_code = int_to_code(self.cao_int)
        self.cao_int += 1
        self.parts.append(Cao(new_code, x, y, z, [zhu], []))
        return new_code

    def add_cao_on_gong_1(self, gong: str, in_or_out: str):
        founded_gong = self.find_part("Gong", gong)
        if founded_gong is None:
            raise ValueError(f"未有栱{gong}。")
        if in_or_out == "内":
            x, y, z = founded_gong.x1, founded_gong.y1, founded_gong.z1
        else:
            x, y, z = founded_gong.x2, founded_gong.y2, founded_gong.z2
        
        new_code = int_to_code(self.cao_int)
        self.cao_int += 1
        self.parts.append(Cao(new_code, x, y, z, [], [gong]))
        return new_code

    def add_ji_on_lin_2(self, lin1: str, in_or_out1: str, lin2: str, in_or_out2: str):
        founded_lins = []
        for lin in [lin1, lin2]:
            founded_lin = self.find_part("Lin", lin)
            if founded_lin is None:
                raise ValueError(f"未有檩{lin}。")
            founded_lins.append(founded_lin)
        base_lins = [lin1, lin2]
        if in_or_out1 == "内":
            (x1, y1, z1), _ = founded_lins[0].endpoints()
        else:
            _, (x1, y1, z1) = founded_lins[0].endpoints()
        if in_or_out2 == "内":
            (x2, y2, z2), _ = founded_lins[1].endpoints()
        else:
            _, (x2, y2, z2) = founded_lins[1].endpoints()
        # if z1 < z2:
        #     x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        #     base_lins[0], base_lins[1] = base_lins[1], base_lins[0]
        # elif z1 == z2:
        #     print(f"置脊于二檩等高者易生错误。请保证相对于建筑主体。前檩{in_or_out1}端位于后檩{in_or_out2}端之内。")
        
        new_code = int_to_code(self.ji_int)
        self.ji_int += 1
        self.parts.append(Ji(new_code, x1, y1, z1, x2, y2, z2, [], [lin1, lin2]))
        return new_code
    
    def add_ji_on_cao_2(self, cao1: str, cao2: str):
        founded_caos = []
        for cao in [cao1, cao2]:
            founded_cao = self.find_part("Cao", cao)
            if founded_cao is None:
                raise ValueError(f"未有檩{cao}。")
            founded_caos.append(founded_cao)
        base_caos = [cao1, cao2]
        x1, y1, z1 = founded_caos[0].x1, founded_caos[0].y1, founded_caos[0].z1
        x2, y2, z2 = founded_caos[1].x1, founded_caos[1].y1, founded_caos[1].z1
        # if z1 < z2:
        #     x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        #     base_caos[0], base_caos[1] = base_caos[1], base_caos[0]
        # elif z1 == z2:
        #     print("置脊于二槽等高者易生错误。请保证相对于建筑主体。前槽位于后槽之内。")
        
        new_code = int_to_code(self.ji_int)
        self.ji_int += 1
        self.parts.append(Ji(new_code, x1, y1, z1, x2, y2, z2, [cao1, cao2], []))
        return new_code

    def add_yan_on_ji_2(self, ji1: str, ji2: str):
        founded_ji = []
        for ji in [ji1, ji2]:
            founded_ji.append(self.find_part("Ji", ji))
        if None in founded_ji:
            raise ValueError(f"未有脊{ji1}或{ji2}。")

        _, (x1, y1, z1) = founded_ji[0].endpoints()
        _, (x2, y2, z2) = founded_ji[1].endpoints()
        
        new_code = int_to_code(self.yan_int)
        self.yan_int += 1
        self.parts.append(Yan(new_code, x1, y1, z1, x2, y2, z2, [ji1, ji2]))
        return new_code