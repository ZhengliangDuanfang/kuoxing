from parts import Zhu, Liang, Lin, JiaoLiang, Fang, BianChuan, FengYan, DouGong
from numbering import int_to_code
import pyvista as pv
import numpy as np

class Structure:
    def __init__(self, save_path: str = "example.txt"):
        self.save_path = save_path
        self.parts = []
        self.insts = []
        self.zhu_int = 0
        self.liang_int = 0
        self.lin_int = 0
        self.jiaoliang_int = 0
        self.fang_int = 0
        self.bianchuan_int = 0
        self.fengyan_int = 0
        self.dougong_int = 0
        self.position = [(2000, -2000, 2000), (0, 1000, 0)]
        self.show_ref = False
        self.plotter = pv.Plotter()

        with open(save_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and len(line) > 0:
                    self.insts.append(line)

    def render(self):
        lines = [p.endpoints() for p in self.parts if not isinstance(p, DouGong)]
        for p in self.parts: 
            if isinstance(p, DouGong):
                lines += p.endpoint_list()
        # print(lines)

        for start, end in lines:
            points = np.array([start, end])
            line = pv.lines_from_points(points)
            self.plotter.add_mesh(line, color='black', line_width=3)
        
        if self.show_ref:
            self.plotter.add_mesh(pv.lines_from_points(np.array([(0, 0, 0), (0, 0, 500)])), color='red', line_width=3)
            self.plotter.add_mesh(pv.lines_from_points(np.array([(0, 0, 0), (0, 500, 0)])), color='blue', line_width=3)
            self.plotter.add_mesh(pv.lines_from_points(np.array([(0, 0, 0), (500, 0, 0)])), color='green', line_width=3)

        position, focus = self.position
        self.plotter.camera_position = [position, focus, (0,0,1)]
        self.plotter.show()

    def dump_insts(self):
        insts = "\n".join(self.insts)
        with open(self.save_path, "w", encoding="utf-8") as f:
            f.write(insts)

    def find_part(self, class_name: str, code: str):
        for part in self.parts:
            if isinstance(part, eval(class_name)) and part.code == code:
                return part
        return None

    def add_zhu_on_di(self, inst: str, x: int, y: int, height: int, radius: int):
        new_code = int_to_code(self.zhu_int)
        self.zhu_int += 1
        self.parts.append(Zhu(new_code, x, y, 0, height, radius, []))
        
        return new_code

    def add_liang_on_zhu(self, inst: str, zhu1: str, zhu2: str, width: int, height: int, in_ext: int, out_ext: int):
        founded_zhus = []
        for zhu in [zhu1, zhu2]:
            founded_zhu = self.find_part("Zhu", zhu)
            if founded_zhu is None:
                raise ValueError(f"柱{zhu}不存在")
            founded_zhus.append(founded_zhu)
        x1, y1 = founded_zhus[0].x, founded_zhus[0].y
        x2, y2 = founded_zhus[1].x, founded_zhus[1].y
        base_zhus = [zhu1, zhu2]
        if x1 != x2 and y1 != y2:
            raise ValueError("梁必须基于2根横坐标或纵坐标相同的柱")
        elif (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            y1, y2 = y2, y1
            x1, x2 = x2, x1
            base_zhus[0], base_zhus[1] = base_zhus[1], base_zhus[0]
        top_z_zhus = min([zhu.z + zhu.height for zhu in founded_zhus])
        new_code = int_to_code(self.liang_int)
        self.liang_int += 1
        self.parts.append(Liang(new_code, x1, x2, y1, y2, top_z_zhus, width, height, in_ext, out_ext, base_zhus))
        
        return new_code

    def add_zhu_on_liang(self, inst: str, liang: str, depth: int, height: int, radius: int):
        founded_liang = self.find_part("Liang", liang)
        if founded_liang is None:
            raise ValueError(f"梁{liang}不存在")
        (x1, y1, z1), (x2, y2, z2) = founded_liang.endpoints()
        if x1 == x2:
            x = x1
            y = y1 + depth
        elif y1 == y2:
            y = y1
            x = x1 + depth
        else:
            raise ValueError("目前只支持横梁与纵梁")
        new_code = int_to_code(self.zhu_int)
        self.zhu_int += 1
        self.parts.append(Zhu(new_code, x, y, z1, height, radius, [liang]))
        
        return new_code

    def add_fang_on_zhu(self, inst: str, zhu1: str, zhu2: str, z: int, width: int, height: int, extend: int):
        founded_zhus = []
        for zhu in [zhu1, zhu2]:
            founded_zhu = self.find_part("Zhu", zhu)
            if founded_zhu is None:
                raise ValueError(f"柱{zhu}不存在")
            founded_zhus.append(founded_zhu)
        x1, y1, z1, h1 = founded_zhus[0].x, founded_zhus[0].y, founded_zhus[0].z, founded_zhus[0].height
        x2, y2, z2, h2 = founded_zhus[1].x, founded_zhus[1].y, founded_zhus[1].z, founded_zhus[1].height
        base_zhus = [zhu1, zhu2]
        if z1 != z2:
            raise ValueError("枋必须基于2根底部高度相同的柱")
        if z > min(h1, h2):
            raise ValueError("枋不能高出两根柱中的任意一根")
        if x1 != x2 and y1 != y2:
            raise ValueError("枋必须基于2根横坐标或纵坐标相同的柱")
        elif (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            y1, y2 = y2, y1
            x1, x2 = x2, x1
            base_zhus[0], base_zhus[1] = base_zhus[1], base_zhus[0]
        new_code = int_to_code(self.fang_int)
        self.fang_int += 1
        self.parts.append(Fang(new_code, x1, x2, y1, y2, z1+z, width, height, extend, base_zhus))
        
        return new_code

    def add_lin_on_zhu(self, inst: str, zhu1: str, zhu2: str, radius: int, extend: int):
        founded_zhus = []
        for zhu in [zhu1, zhu2]:
            founded_zhu = self.find_part("Zhu", zhu)
            if founded_zhu is None:
                raise ValueError(f"柱{zhu}不存在")
            founded_zhus.append(founded_zhu)
        x1, y1, z1, h1 = founded_zhus[0].x, founded_zhus[0].y, founded_zhus[0].z, founded_zhus[0].height
        x2, y2, z2, h2 = founded_zhus[1].x, founded_zhus[1].y, founded_zhus[1].z, founded_zhus[1].height
        base_zhus = [zhu1, zhu2]
        if z1+h1 != z2+h2:
            raise ValueError("檩必须基于2根顶端高度相同的柱")
        if x1 != x2 and y1 != y2:
            raise ValueError("檩必须基于2根横坐标或纵坐标相同的柱")
        elif (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            y1, y2 = y2, y1
            x1, x2 = x2, x1
            base_zhus[0], base_zhus[1] = base_zhus[1], base_zhus[0]
        z = z1+h1
        new_code = int_to_code(self.lin_int)
        self.lin_int += 1
        self.parts.append(Lin(new_code, x1, x2, y1, y2, z, radius, extend, base_zhus, []))
        
        return new_code

    def add_jiaoliang_on_zhu(self, inst: str, zhu1:str, zhu2:str, width: int, height: int):
        founded_zhus = []
        for zhu in [zhu1, zhu2]:
            founded_zhu = self.find_part("Zhu", zhu)
            if founded_zhu is None:
                raise ValueError(f"柱{zhu}不存在")
            founded_zhus.append(founded_zhu)
        base_zhus = [zhu1, zhu2]
        _, (x1, y1, z1) = founded_zhus[0].endpoints()
        _, (x2, y2, z2) = founded_zhus[1].endpoints()
        if z1 <= z2:
            founded_zhus[0], founded_zhus[1] = founded_zhus[1], founded_zhus[0]
            base_zhus[0], base_zhus[1] = base_zhus[1], base_zhus[0]
            _, (x1, y1, z1) = founded_zhus[0].endpoints()
            _, (x2, y2, z2) = founded_zhus[1].endpoints()
        if x1 == x2 or y1 == y2:
            raise ValueError("角梁必须基于2根横纵不相同的柱")
        
        new_code = int_to_code(self.jiaoliang_int)
        self.jiaoliang_int += 1
        self.parts.append(JiaoLiang(new_code, x1, x2, y1, y2, z1, z2, width, height, base_zhus, []))
        
        return new_code

    def add_bianchuan_on_lin(self, inst: str, lin1: str, lin2: str, flag_1: bool, flag_2: bool):
        founded_lins = []
        for lin in [lin1, lin2]:
            founded_lin = self.find_part("Lin", lin)
            if founded_lin is None:
                raise ValueError(f"檩{lin}不存在")
            founded_lins.append(founded_lin)
        (x1, y1, z1), (x2, y2, z2) = founded_lins[0].endpoints()
        (x3, y3, z3), (x4, y4, z4) = founded_lins[1].endpoints()
        new_x1, new_y1, new_z1 = (x1, y1, z1) if flag_1 else (x2, y2, z2)
        new_x2, new_y2, new_z2 = (x3, y3, z3) if flag_2 else (x4, y4, z4)
        new_code = int_to_code(self.bianchuan_int)
        self.bianchuan_int += 1
        self.parts.append(BianChuan(new_code, new_x1, new_x2, new_y1, new_y2, new_z1, new_z2, [lin1, lin2]))
        
        return new_code
    
    def add_dougong_on_liang(self, inst:str, liang: str, depth:int, dx1:int, dy1:int, dz1:int, dx2:int, dy2:int, dz2:int):
        founded_liang = self.find_part("Liang", liang)
        if founded_liang is None:
            raise ValueError(f"梁{liang}不存在")
        (x1, y1, z1), (x2, y2, z2) = founded_liang.endpoints()
        if x1 == x2:
            y1 = y1 + depth
        elif y1 == y2:
            x1 = x1 + depth
        else:
            raise ValueError("目前只支持横梁与纵梁")
        new_code = int_to_code(self.dougong_int)
        self.dougong_int += 1
        self.parts.append(DouGong(new_code, x1, y1, z1, x1+dx1, y1+dy1, z1+dz1, x1+dx2, y1+dy2, z1+dz2, [founded_liang]))
        
        return new_code
        
    def add_lin_on_dougong(self, inst: str, dougong1: str, side1: int, dougong2: str, side2: int, radius:int, extend:int):
        founded_dougongs = []
        for dougong in [dougong1, dougong2]:
            founded_dougong = self.find_part("DouGong", dougong)
            if founded_dougong is None:
                raise ValueError(f"柱{dougong}不存在")
            founded_dougongs.append(founded_dougong)
        if side1 == 1:
            x1, y1, z1 = founded_dougongs[0].x1, founded_dougongs[0].y1, founded_dougongs[0].z1
        else:
            x1, y1, z1 = founded_dougongs[0].x2, founded_dougongs[0].y2, founded_dougongs[0].z2
        if side2 == 1:
            x2, y2, z2 = founded_dougongs[1].x1, founded_dougongs[1].y1, founded_dougongs[1].z1
        else:
            x2, y2, z2 = founded_dougongs[1].x2, founded_dougongs[1].y2, founded_dougongs[1].z2
        base_dougongs = [dougong1, dougong2]
        if z1 != z2:
            raise ValueError("檩必须基于2根顶端高度相同的斗拱")
        if x1 != x2 and y1 != y2:
            raise ValueError("檩必须基于2根横坐标或纵坐标相同的柱")
        elif (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            y1, y2 = y2, y1
            x1, x2 = x2, x1
            base_dougongs[0], base_dougongs[1] = base_dougongs[1], base_dougongs[0]
        z = z1
        new_code = int_to_code(self.lin_int)
        self.lin_int += 1
        self.parts.append(Lin(new_code, x1, x2, y1, y2, z, radius, extend, [], base_dougongs))
        
        return new_code
    
    def add_jiaoliang_on_dougong(self, inst: str, dougong:str, width: int, height: int):
        founded_dougong = self.find_part("DouGong", dougong)
        if founded_dougong is None:
            raise ValueError(f"斗拱{dougong}不存在")
        (x1, y1, z1), (x2, y2, z2) = founded_dougong.tops()
        if z1 <= z2:
            x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
        
        new_code = int_to_code(self.jiaoliang_int)
        self.jiaoliang_int += 1
        self.parts.append(JiaoLiang(new_code, x1, x2, y1, y2, z1, z2, width, height, [], [founded_dougong]))
        
        return new_code
    
    def add_jiaoliang_out_zhu_to_dougong(self, inst: str, zhu:str, dougong:str, side:int, width: int, height: int):
        founded_dougong = self.find_part("DouGong", dougong)
        if founded_dougong is None:
            raise ValueError(f"斗拱{dougong}不存在")
        founded_zhu = self.find_part("Zhu", zhu)
        if founded_zhu is None:
            raise ValueError(f"柱{zhu}不存在")

        if side == 1:
            (x2, y2, z2), _ = founded_dougong.tops()
        else:
            _, (x2, y2, z2) = founded_dougong.tops()
        _, (x1, y1, z1) = founded_zhu.endpoints()
        if z1 <= z2:
            raise ValueError(f"对于角梁，不接受柱低于斗拱")
        
        new_code = int_to_code(self.jiaoliang_int)
        self.jiaoliang_int += 1
        self.parts.append(JiaoLiang(new_code, x1, x2, y1, y2, z1, z2, width, height, [founded_zhu], [founded_dougong]))
        
        return new_code
    
    def add_fengyan_on_dougong(self, inst:str, dougong1: str, side1: int, dougong2: str, side2: int, width:int, height:int):
        founded_dougongs = []
        for dougong in [dougong1, dougong2]:
            founded_dougong = self.find_part("DouGong", dougong)
            if founded_dougong is None:
                raise ValueError(f"柱{dougong}不存在")
            founded_dougongs.append(founded_dougong)
        if side1 == 1:
            (x1, y1, z1), _ = founded_dougongs[0].tops()
        else:
            _, (x1, y1, z1) = founded_dougongs[0].tops()
        if side2 == 1:
            (x2, y2, z2), _ = founded_dougongs[1].tops()
        else:
            _, (x2, y2, z2) = founded_dougongs[1].tops()
        new_code = int_to_code(self.fengyan_int)
        self.fengyan_int += 1
        self.parts.append(FengYan(new_code, x1, x2, y1, y2, z1, z2, width, height, [dougong1, dougong2]))
        
        return new_code