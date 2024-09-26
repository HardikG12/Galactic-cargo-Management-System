from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.bin_storage_bin_id = AVLTree()
        self.bin_storage_capacity = AVLTree()
        self.object_storage = AVLTree()
        self.count_bin = 0
        self.count_object = 0

    def add_bin(self, bin_id, capacity):
        
        b = Bin(bin_id,capacity)
        self.bin_storage_capacity.insert((b.remaining,b.bin_id),b)
        self.bin_storage_bin_id.insert((b.bin_id,0),b)
        self.count_bin += 1

    def add_object(self, object_id, size, color):
        obj = Object(object_id, size, color)

        if color == Color.BLUE:
            b = self.bin_storage_capacity._blue_cargo(self.bin_storage_capacity.root, size)
        elif color == Color.YELLOW:
            b = self.bin_storage_capacity._yellow_cargo(self.bin_storage_capacity.root, size)
            
        elif color == Color.RED:
            b = self.bin_storage_capacity._red_cargo(self.bin_storage_capacity.root, size)
        else:
            b = self.bin_storage_capacity._green_cargo(self.bin_storage_capacity.root, size)

        if b is None:
            raise NoBinFoundException

        x = b.value

        
        self.bin_storage_capacity.remove((x.remaining,x.bin_id))

        x.add_object(obj)

        self.bin_storage_capacity.insert((x.remaining,x.bin_id),x)

        self.object_storage.insert((object_id, 0), obj)
        self.count_object += 1
        
    
    def delete_object(self, object_id):
        o = self.object_storage.find(self.object_storage.root,(object_id,0))
        if o is None:
            raise ValueError()
        b = o.bin
        self.bin_storage_capacity.remove((b.remaining,b.bin_id))
        b.remove_object(object_id)
        self.bin_storage_capacity.insert((b.remaining,b.bin_id),b)
        
        self.count_object-=1
        self.object_storage.remove((object_id,0))
        
        # Implement logic to remove an object from its bin

    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        b = self.bin_storage_bin_id.find(self.bin_storage_bin_id.root,(bin_id,0))
        return (b.remaining,b.object_list())
        

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        o = self.object_storage.find(self.object_storage.root,(object_id,0))
        if o is None:
            return None
        return o.bin.bin_id
    
    def show_bins(self):
        self.bin_storage_capacity.inorder(self.bin_storage_capacity.root)
        print()