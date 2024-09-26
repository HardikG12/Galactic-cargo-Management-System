from node import Node

def comp_1(node_1, node_2):
    if node_1.key[0] == node_2.key[0]:
        return node_1.key[1] > node_2.key[1]
    return node_1.key[0] > node_2.key[0]

class AVLTree:
    
    def __init__(self, compare_function=comp_1):
        self.root = None
        self.node_count = 0
        self.compare = compare_function
    
    def get_height(self, current_node):
        if current_node is None:
            return 0
        return current_node.height
        
    def is_balanced(self, current_node):
        return abs(self.get_height(current_node.left) - self.get_height(current_node.right)) <= 1
    
    def update_height(self, current_node):
        if current_node is not None:
            current_node.height = 1 + max(self.get_height(current_node.left), self.get_height(current_node.right))
            
    def balance_factor(self, current_node):
        return self.get_height(current_node.left) - self.get_height(current_node.right)

    def rotate_left(self, z_node):
        y_node = z_node.right
        temp_left = y_node.left

        y_node.left = z_node
        z_node.right = temp_left

        self.update_height(z_node)
        self.update_height(y_node)

        return y_node

    def rotate_right(self, z_node):
        y_node = z_node.left
        temp_right = y_node.right

        y_node.right = z_node
        z_node.left = temp_right

        self.update_height(z_node)
        self.update_height(y_node)

        return y_node
        
    def rebalance(self, current_node):
        self.update_height(current_node)
        bal_factor = self.balance_factor(current_node)

        # Left-heavy case
        if bal_factor > 1:
            if self.balance_factor(current_node.left) >= 0:
                return self.rotate_right(current_node)
            else:
                current_node.left = self.rotate_left(current_node.left)
                return self.rotate_right(current_node)

        # Right-heavy case
        if bal_factor < -1:
            if self.balance_factor(current_node.right) <= 0:
                return self.rotate_left(current_node)
            else:
                current_node.right = self.rotate_right(current_node.right)
                return self.rotate_left(current_node)

        return current_node
    
    def insert(self, key, value):
        self.root = self._insert_node(self.root, key, value)
        self.node_count += 1
        
    def remove(self, key):
        if self.root is None:
            return
        self.root = self._delete_node(self.root, key)
        if self.root is not None:
            self.node_count -= 1
    
    def _insert_node(self, current_node, key, value):
        if current_node is None:
            return Node(key, value)
        if self.compare(current_node,Node(key, value)):
            current_node.left = self._insert_node(current_node.left, key, value)
        else:
            current_node.right = self._insert_node(current_node.right, key, value)

        self.update_height(current_node)
        
        return self.rebalance(current_node)
        
    def _min_node(self, current_node):
        if current_node is None or current_node.left is None:
            return current_node
        return self._min_node(current_node.left)
        
    def _delete_node(self, current_node, key):
        if current_node is None:
            return None
        
        if self.compare(current_node,Node(key, 0)):
            current_node.left = self._delete_node(current_node.left, key)
        elif self.compare(Node(key, 0),current_node):
            current_node.right = self._delete_node(current_node.right, key)
        else:
            if current_node.left is None:
                return current_node.right
            if current_node.right is None:
                return current_node.left
            
            temp_node = self._min_node(current_node.right)
            current_node.key = temp_node.key
            current_node.value = temp_node.value
            current_node.right = self._delete_node(current_node.right, temp_node.key)   

        self.update_height(current_node)
        
        return self.rebalance(current_node)
        
    def traverse_tree(self, root, result_list):
        if root is None:
            return []
        
        self.traverse_tree(root.left,result_list)
        result_list.append(root.key[0])
        self.traverse_tree(root.right,result_list)
        return result_list
        
    def find(self, root, key):
        if root is None:
            return None
        if root.key == key:
            return root.value
        elif self.compare(root, Node(key, 0)):
            return self.find(root.left, key)
        return self.find(root.right, key)

    def _least_cap_greatest_id(self, node, v):
        a = node

        while node is not None:
            if node.key[0]<v:
                node = node.right
            elif node.key[0]>v:
                node = node.left
            elif node.key[0]==v:
                a = node
                node = node.right
        
        return a
    
    def _greatest_cap_least_id(self, node, v):
        a = node

        while node is not None:
            if node.key[0]<v:
                node = node.right
            elif node.key[0]>v:
                node = node.left
            elif node.key[0]==v:
                a = node
                node = node.left
        
        return a
        
    def _compact_cap(self, node, v):
        a = node
        c= None
        while a is not None:
            if a.key[0]<v:
                a = a.right
            else:
                if c is None or a.key[0]<c.key[0]:
                    c = a
                elif a.key[0]==c.key[0] and (a.key[1]<c.key[1]):
                    c = a
                a = a.left
            
        return c
    
    def _largest_fit(self, node, v):
        if node is None:
            return None
        elif node.right is None:
            if node.key[0]<v:
                return None
            return node
        return self._largest_fit(node.right, v)
    
    # Cargo-related methods
    def _blue_cargo(self, root, s):
        return self._compact_cap(root, s)
        
    def _yellow_cargo(self, root, s):
        h = root
        node = self._compact_cap(root, s)
        if node is None:
            return None
        return self._least_cap_greatest_id(h, node.key[0])

    def _green_cargo(self, root, s):
        return self._largest_fit(root, s)

    def _red_cargo(self, root, s):
        node = self._largest_fit(root, s)
        if node is None:
            return None
        return self._greatest_cap_least_id(root, node.key[0])
    
    def inorder(self,node):
        if node is None:
            return

        self.inorder(node.left)
        print(node.key,end=" ")
        self.inorder(node.right)