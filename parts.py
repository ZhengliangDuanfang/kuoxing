class Part:
    def __init__(self, code: str):
        self.code = code

class Zhu(Part):
    def __init__(self, code: str, x: int, y: int, z: int, height: int, radius: int, base_liang: list[str]):
        if not isinstance(base_liang, list) or len(base_liang) > 2 or len(base_liang) < 0:
            raise ValueError("柱基于的梁的数量应为0或1")
        if len(base_liang) == 0:
            if z != 0:
                raise ValueError("如果柱不基于梁，必须基于地")
        super().__init__(code)
        self.x = x
        self.y = y
        self.z = z
        self.height = height
        self.radius = radius
        self.base_liang = base_liang
    
    def endpoints(self):
        return (self.x, self.y, self.z), (self.x, self.y, self.z + self.height)

class Liang(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, width: int, height: int, ext1: int, ext2: int, base_zhu: list[str]):
        if not isinstance(base_zhu, list) or len(base_zhu) != 2:
            raise ValueError("梁必须基于2根柱")
        if not ((x1 == x2 and y1 < y2) or (y1 == y2 and x1 < x2)):
            raise ValueError("梁必须为横梁或纵梁")
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z = z
        self.width = width
        self.height = height
        self.ext1 = ext1
        self.ext2 = ext2
        self.base_zhu = base_zhu

    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.ext1, self.z), (self.x2, self.y2 + self.ext2, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.ext1, self.y1, self.z), (self.x2 + self.ext2, self.y2, self.z)
        else:
            raise ValueError("目前只支持横梁与纵梁")

class Fang(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, width: int, height: int, extend: int, base_zhu: list[str]):
        if not isinstance(base_zhu, list) or len(base_zhu) != 2:
            raise ValueError("枋必须基于2根柱")
        if not ((x1 == x2 and y1 < y2) or (y1 == y2 and x1 < x2)):
            raise ValueError("枋必须为横枋或纵枋")
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z = z
        self.width = width
        self.height = height
        self.extend = extend
        self.base_zhu = base_zhu
    
    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.extend, self.z), (self.x2, self.y2 + self.extend, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.extend, self.y1, self.z), (self.x2 + self.extend, self.y2, self.z)
        else:
            raise ValueError("目前只支持横枋与纵枋")

class Lin(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, radius: int, extend: int, base_zhu: list[str], base_dougong: list[str]):
        if (not isinstance(base_zhu, list) or len(base_zhu) != 2) and (not isinstance(base_dougong, list) or len(base_dougong) != 2):
            raise ValueError("檩必须基于2根柱或斗拱")
        if not ((x1 == x2 and y1 < y2) or (y1 == y2 and x1 < x2)):
            raise ValueError("檩必须为横檩或纵檩")
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z = z
        self.radius = radius
        self.extend = extend
        self.base_zhu = base_zhu
    
    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.extend, self.z), (self.x2, self.y2 + self.extend, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.extend, self.y1, self.z), (self.x2 + self.extend, self.y2, self.z)
        else:
            raise ValueError("目前只支持横檩与纵檩")

class JiaoLiang(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int, width: int, height: int, base_zhu: list[str], base_dougong: list[str]):
        if (not isinstance(base_zhu, list)) or not ((len(base_zhu) == 2 and len(base_dougong) == 0) or (len(base_zhu) == 0 and len(base_dougong) == 1) or (len(base_zhu) == 1 and len(base_dougong) == 1)):
            raise ValueError("角梁必须基于2根柱或1根柱1斗拱或1斗拱")
        if len(base_zhu) == 2 and z1 <= z2:
            raise ValueError("如果有2根柱，角梁必须基于较高的柱")
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.width = width
        self.height = height
        self.base_zhu = base_zhu

    def endpoints(self):
        return (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2)

class BianChuan(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int, base_lin: list[str]):
        if not isinstance(base_lin, list) or (len(base_lin) != 2):
            raise ValueError("边椽必须基于2根檩")
        if not (x1 == x2 or y1 == y2):
            raise ValueError("边椽必须为横边椽或纵边椽")
        if len(base_lin) == 2 and z1 <= z2:
            raise ValueError("如果有2根檩，边椽必须基于较高的檩")
        
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.base_lin = base_lin

    def endpoints(self):
        return (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2)

class FengYan(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z1:int, z2: int, width: int, height: int, base_dougong: list[str]):
        if not isinstance(base_dougong, list) or (len(base_dougong) != 2):
            raise ValueError("封檐必须基于2个斗拱")
        if not (x1 == x2 or y1 == y2):
            raise ValueError("封檐必须为横或纵封檐")
        
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.width = width
        self.height = height
    
    def endpoints(self):
        return (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2)

class DouGong(Part):
    def __init__(self, code: str, x0:int, y0:int, z0:int, x1:int, y1:int, z1:int, x2:int, y2:int, z2:int, base_liang: list[str]):
        if not isinstance(base_liang, list) or len(base_liang) != 1:
            raise ValueError("斗拱必须基于1根梁")
        super().__init__(code)
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.base_liang = base_liang
    
    def tops(self):
        return (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2)
    
    def endpoint_list(self):
        return [((self.x1, self.y1, self.z1), (self.x0, self.y0, self.z0)), ((self.x0, self.y0, self.z0), (self.x2, self.y2, self.z2))]
