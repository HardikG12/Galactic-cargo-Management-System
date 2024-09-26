from avl import AVLTree
from object import Object

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.data = AVLTree()
        self.remaining = capacity
        pass

    def add_object(self, object):
        # Implement logic to add an object to this bin
        self.data.insert((object.object_id,0),object)
        self.remaining -= object.size
        object.bin = self

    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        ob = self.data.find(self.data.root,(object_id,0))
        if ob is None:
            return None
        self.remaining += ob.size
        self.data.remove((object_id,0))
    
    def object_list(self):
        return self.data.traverse_tree(self.data.root,[])