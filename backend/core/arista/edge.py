if __package__.startswith("backend."):
    from ..vertice.vertex import vertex
else:
    from core.vertice.vertex import vertex
class edge:
    def __init__(self,v1:vertex,v2:vertex, weight:int):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight

    def get_v1(self):
        return self.v1

    def get_v2(self):
        return self.v2

    def get_weight(self):
        return self.weight
    def set_weight(self,weight):
        self.weight = weight

    