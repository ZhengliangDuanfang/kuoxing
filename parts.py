class Part:
    def __init__(self, code: str):
        self.code = code

class Zhu(Part):
    def __init__(self, code: str, x: int, y: int, z: int, height: int):
        if height == 0:
            raise ValueError("柱不可始终共点。")
        super().__init__(code)
        self.x = x
        self.y = y
        self.z = z
        self.height = height
        self.color = "black"
    
    def endpoints(self):
        return (self.x, self.y, self.z), (self.x, self.y, self.z + self.height)

class Liang(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, ext1: int, ext2: int):
        if x1 == x2 and y1 == y2:
            raise ValueError("梁不可始终共点。")
        if x1 != x2 and y1 != y2:
            raise ValueError("梁需并于横轴。或于纵轴。此程序之失也，请报告之。")
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
        self.color = "black"

    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.ext1, self.z), (self.x2, self.y2 + self.ext2, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.ext1, self.y1, self.z), (self.x2 + self.ext2, self.y2, self.z)
        else:
            raise ValueError("此梁非并于横轴或纵轴者。")

class Gong(Part):
    def __init__(self, code: str, x0:int, y0:int, z0:int, x1:int, y1:int, z1:int, x2:int, y2:int, z2:int):
        if (x1 - x0 == 0 and y1 - y0 == 0 and z1 - z0 == 0) or (x2 - x0 == 0 and y2 - y0 == 0 and z2 - z0 == 0):
            raise ValueError("栱不可倾于一隅。")
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
        self.color = "black"
    
    def tops(self):
        return (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2)
    
    def endpoint_list_with_color(self):
        return [(self.color, ((self.x1, self.y1, self.z1), (self.x0, self.y0, self.z0))), (self.color, ((self.x0, self.y0, self.z0), (self.x2, self.y2, self.z2)))]

class Fang(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, ext1: int, ext2: int):
        if x1 == x2 and y1 == y2:
            raise ValueError("枋不可始终共点。")
        if x1 != x2 and y1 != y2:
            raise ValueError("枋需并于横轴。或于纵轴。此程序之失也，请报告之。")
        if (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            raise ValueError("枋之始终有内外之分。此程序之失也，请报告之。")
        
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z = z
        self.ext1 = ext1
        self.ext2 = ext2
        self.color = "black"
    
    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.ext1, self.z), (self.x2, self.y2 + self.ext2, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.ext1, self.y1, self.z), (self.x2 + self.ext2, self.y2, self.z)
        else:
            raise ValueError("此枋非并于横轴或纵轴者。")

class Lin(Part):
    def __init__(self, code: str, x1: int, x2: int, y1: int, y2: int, z: int, extend: int):
        if x1 == x2 and y1 == y2:
            raise ValueError("檩不可始终共点。")
        if x1 != x2 and y1 != y2:
            raise ValueError("檩需并于横轴。或于纵轴。此程序之失也，请报告之。")
        if (x1 == x2 and y1 > y2) or (y1 == y2 and x1 > x2):
            raise ValueError("檩之始终有内外之分。此程序之失也，请报告之。")
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z = z
        self.extend = extend
        self.color = "black"
    
    def endpoints(self):
        if self.x1 == self.x2:
            return (self.x1, self.y1 - self.extend, self.z), (self.x2, self.y2 + self.extend, self.z)
        elif self.y1 == self.y2:
            return (self.x1 - self.extend, self.y1, self.z), (self.x2 + self.extend, self.y2, self.z)
        else:
            raise ValueError("此檩非并于横轴或纵轴者。")

class Dian(Part):
    def __init__(self, code: str, x1: int, y1: int, z1: int):
        super().__init__(code)
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.color = "black"
    
    def endpoint(self):
        return (self.x1, self.y1, self.z1)

class Ding(Part):
    def __init__(self, code: str, pos_list: list[tuple[int, int, int]]):
        if not len(pos_list) == 3 and not len(pos_list) == 4:
            raise ValueError("置顶需于点三。或于点四。此程序之失也，请报告之。")
        super().__init__(code)
        self.pos_list = pos_list
        self.color = "black"
    
    def triangle_list_with_color(self):
        if len(self.pos_list) == 3:
            return [(self.color, self.pos_list[0], self.pos_list[1], self.pos_list[2])]
        elif len(self.pos_list) == 4:
            return [(self.color, self.pos_list[0], self.pos_list[1], self.pos_list[2]), (self.color, self.pos_list[1], self.pos_list[2], self.pos_list[3])]
        else:
            raise ValueError("顶未连接任何点。此程序之失也，请报告之。")

class Ji(Part):
    def __init__(self, code: str, pos_list: list[tuple[int, int, int]]):
        if not len(pos_list) == 2:
            raise ValueError("置脊需于点二。此程序之失也，请报告之。")
        super().__init__(code)
        self.pos_list = pos_list
        self.color = "black"

    def endpoints(self):
        return self.pos_list[0], self.pos_list[1]

class Wall(Part):
    def __init__(self, code: str, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, type_name: str):
        if x1 == x2 and y1 == y2 and z1 == z2:
            raise ValueError("墙之两端点不可全同。")
        if (x1 == x2 and y1 == y2) or (z1 == z2 and y1 == y2) or (z1 == z2 and x1 == x2):
            raise ValueError("墙之两端点不可共轴。")
        if z1 == z2:
            raise ValueError("墙高不可为零。")
        if type_name not in ["rect", "tri"]:
            raise ValueError("不合法墙类型。此程序之失也，请报告之。")
        super().__init__(code)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.color = "#ff4500"
        self.type_name = type_name
    
    def triangle_list_with_color(self):
        if self.type_name == "rect":
            return [(self.color, (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2), (self.x1, self.y1, self.z2)), (self.color, (self.x2, self.y2, self.z2), (self.x2, self.y2, self.z1), (self.x1, self.y1, self.z1))]
        elif self.type_name == "tri":
            return [(self.color, (self.x1, self.y1, self.z1), (self.x2, self.y2, self.z2), (self.x1, self.y1, self.z2))]
        else:
            raise ValueError("不合法墙类型。此程序之失也，请报告之。")
