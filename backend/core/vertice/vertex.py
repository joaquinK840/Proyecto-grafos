class vertex:
    def __init__(self,name:int,available=True):
        """objeto tipo vertice"""
        self.name = name
        self.neighbors = []
        self.available = available

    def get_name(self):
        """get del ID"""
        return self.name
    def set_name(self,name):
        self.name = name

    def get_neighbors(self):
        return self.neighbors
    def add_neighbors(self,neighbor):
        self.neighbors.append(neighbor)


    def get_available(self):
        return self.available
    def set_available(self, available):
        self.available =available


