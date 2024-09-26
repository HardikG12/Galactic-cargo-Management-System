class Node:
    
    def __init__(self,key,value):
        
        self.height = 1
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        
    def left_height(self):
        if self.left is not None:
            return self.left.height
        return -1
        
    def right_height(self):
        if self.right is not None:
            return self.right.height
        return -1