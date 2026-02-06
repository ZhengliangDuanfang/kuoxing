class Part:
    def __init__(self, code: str):
        self.code = code

class Zhu(Part):
    def __init__(self, code: str, x: int, y: int, z: int, height: int,  base_liang: list[str], base_gong: list[str]):
        if height == 0:
            raise ValueError("柱不可始终共点。")
        if (not (len(base_liang) == 1 and len(base_gong) == 0)) and (not (len(base_liang) == 0 and len(base_gong) == 1)) and (not (len(base_liang) == 0 and len(base_gong) == 0)):
            raise ValueError("置柱需于地。或于梁一。或于栱一。此程序之失也，请报告之。")
        if len(base_liang) == 0 and z != 0:
            raise ValueError("若置柱不于梁或栱。需于地。此程序之失也，请报告之。")
        super().__init__(code)
        self.x = x
        self.y = y
        self.z = z
        self.height = height
        self.base_liang = base_liang
        self.base_gong = base_gong
    
    def endpoints(self):
        return (self.x, self.y, self.z), (self.x, self.y, self.z + self.height)

class Liang(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, ext1: int, ext2: int, base_zhu: list[str]):
        if x1 == x2 and y1 == y2:
            raise ValueError("梁不可始终共点。")
        if x1 != x2 and y1 != y2:
            raise ValueError("梁需并于横轴。或于纵轴。此程序之失也，请报告之。")
        if not len(base_zhu) == 2:
            raise ValueError("置梁需于柱二。此程序之失也，请报告之。")
        if (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            raise ValueError("梁之始终有内外之分。此程序之失也，请报告之。")
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z = z
        self.ext1 = ext1
        self.ext2 = ext2
        self.base_zhu = base_zhu

    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.ext1, self.z), (self.x2, self.y2 + self.ext2, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.ext1, self.y1, self.z), (self.x2 + self.ext2, self.y2, self.z)
        else:
            raise ValueError("此梁非并于横轴或纵轴者。")

class Gong(Part):
    def __init__(self, code: str, x0:int, y0:int, z0:int, x1:int, y1:int, z1:int, x2:int, y2:int, z2:int, base_liang: list[str]):
        if (x1 - x0 == 0 and y1 - y0 == 0 and z1 - z0 == 0) or (x2 - x0 == 0 and y2 - y0 == 0 and z2 - z0 == 0):
            raise ValueError("栱不可倾于一隅。")
        if not len(base_liang) == 1:
            raise ValueError("置栱需于梁一。此程序之失也，请报告之。")
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

class Fang(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, ext1: int, ext2: int, base_zhu: list[str]):
        if x1 == x2 and y1 == y2:
            raise ValueError("枋不可始终共点。")
        if x1 != x2 and y1 != y2:
            raise ValueError("枋需并于横轴。或于纵轴。此程序之失也，请报告之。")
        if (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            raise ValueError("枋之始终有内外之分。此程序之失也，请报告之。")
        if len(base_zhu) != 2:
            raise ValueError("置枋需于柱二。此程序之失也，请报告之。")
        
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z = z
        self.ext1 = ext1
        self.ext2 = ext2
        self.base_zhu = base_zhu
    
    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.ext1, self.z), (self.x2, self.y2 + self.ext2, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.ext1, self.y1, self.z), (self.x2 + self.ext2, self.y2, self.z)
        else:
            raise ValueError("此枋非并于横轴或纵轴者。")

class Lin(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, extend: int, base_zhu: list[str], base_gong: list[str]):
        if x1 == x2 and y1 == y2:
            raise ValueError("檩不可始终共点。")
        if x1 != x2 and y1 != y2:
            raise ValueError("檩需并于横轴。或于纵轴。此程序之失也，请报告之。")
        if (not len(base_zhu) == 2) and (not len(base_gong) == 2):
            raise ValueError("置檩需于柱二。或于栱二。此程序之失也，请报告之。")
        if (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            raise ValueError("檩之始终有内外之分。此程序之失也，请报告之。")
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z = z
        self.extend = extend
        self.base_zhu = base_zhu
    
    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.extend, self.z), (self.x2, self.y2 + self.extend, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.extend, self.y1, self.z), (self.x2 + self.extend, self.y2, self.z)
        else:
            raise ValueError("此檩非并于横轴或纵轴者。")

class Cao(Part):
    def __init__(self, code: str, x1: int, y1: int, z1: int, base_zhu: list[str], base_gong: list[str]):
        if not len(base_zhu) == 1 and not len(base_gong) == 1:
            raise ValueError("置槽需于柱一。或于栱一。此程序之失也，请报告之。")
        super().__init__(code)
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.base_zhu = base_zhu
        self.base_gong = base_gong

class Ji(Part):
    def __init__(self, code: str, x1: int, y1: int, z1: int, x2: int, y2: int, z2:int, base_cao: list[str], base_lin: list[str]):
        if x1 == x2 and y1 == y2:
            raise ValueError("脊不可始终共点。或直垂于地。")
        if (not len(base_cao) == 2) and (not len(base_lin) == 2):
            raise ValueError("置脊需于槽二。或于檩二。此程序之失也，请报告之。")
        super().__init__(code)
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.base_cao = base_cao
    
    def endpoints(self):
        return (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2)

class Yan(Part):
    def __init__(self, code: str, x1: int, y1: int, z1: int, x2: int, y2: int, z2:int, base_ji: list[str]):
        if x1 == x2 and y1 == y2:
            raise ValueError("檐不可始终共点。或直垂于地。")
        if not len(base_ji) == 2:
            raise ValueError("置檐需于脊二。此程序之失也，请报告之。")
        super().__init__(code)
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.base_ji = base_ji

    def endpoints(self):
        return (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2)