class stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("no se puede retirar un elemento de una pila vacia")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("no se puede consultar una pila vacia")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
