import math  

class vec2i:
    
    def __init__(self, width: int = 0, length: int = 0):
        self.x = width
        self.y = length

    def distance(self, other):
        x : float = other.x - self.x;
        y : float = other.y - self.y;
        return math.sqrt(x * x + y * y);

    def __add__(self, o): 
        a = vec2i(self.x + o.x, self.y + o.y)
        return a

    def __eq__(self, o): 
        if(self.x == o.x and self.y == o.y):
            return True
        else:
            return False

