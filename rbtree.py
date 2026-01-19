import sys

class Node:
    data = 0
    value = None
    color = ''
    left, right, parent = None, None, None

    def __init__(self, key, value):
        self.data = self.normalize_keys(key)
        self.value = value
        self.size = self.compute_size()
        self.color = 'Red'
        self.left = None
        self.right = None
        self.parent = None
    
    def normalize_keys(self, key):
        if isinstance(key, int):
            return (0, key)
        if isinstance(key, str):
            return (1, key)
        else:
            raise TypeError('Unsupported Key Type')
        
    def get_deep_sizeof(self, obj, seen=None):
        if seen == None:
            seen = set()
        
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        seen.add(obj_id)

        size = sys.getsizeof(obj)

        if isinstance(obj, dict):
            size += sum( (self.get_deep_sizeof(k, seen) + self.get_deep_sizeof(v, seen) for k, v in obj.items()))
        elif isinstance(obj, (list, tuple, set)):
            size += sum(self.get_deep_sizeof(i, seen) for i in obj)
        
        return size

    
    def compute_size(self):
        key_size = self.get_deep_sizeof(self.data)
        value_size = self.get_deep_sizeof(self.value)

        return key_size + value_size


class RBTree:
    root = None #5
    size = 0

    def __init__(self):
        pass

    def leftRotate(self, node):
        y = node.right
        node.right = y.left
        if y.left != None:
            y.left.parent = node
        y.parent = node.parent
        if node.parent == None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y

        y.left = node
        node.parent = y

    def rightRotate(self, node):
        y = node.left
        node.left = y.right
        if y.right != None:
            y.right.parent = node
        y.parent = node.parent

        if node.parent == None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y

        y.right = node
        node.parent = y

        

    def fixInsert(self, node:Node):
        # print(node.data)
        # print(node.parent)
        while node != self.root and node.parent and node.parent.color == 'Red':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle is not None and uncle.color == 'Red':
                    node.parent.color = 'Black'
                    uncle.color = 'Black'
                    node.parent.parent.color = 'Red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.leftRotate(node)
                    node.parent.color = 'Black'
                    node.parent.parent.color = 'Red'
                    self.rightRotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle is not None and uncle.color == 'Red':
                    node.parent.color = "Black"
                    uncle.color = "Black"
                    node.parent.parent.color = 'Red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rightRotate(node)
                    node.parent.color = 'Black'
                    node.parent.parent.color = 'Red'
                    self.leftRotate(node.parent.parent)


        self.root.color = 'Black' 

    
    def inorder_helper(self, node):
        if node != None:
            self.inorder_helper(node.left)
            print(node.data, '-', node.value)
            self.inorder_helper(node.right)

    def insert(self, key, data):
        node = Node(key=key, value=data)
        self.size += node.size

        if self.root == None:
            node.color = 'Black'
            self.root = node
            return
        
        current = self.root

        while current:
            parent = current #5
            if node.data < current.data:
                current = current.left
            else:
                current = current.right
        
        node.parent = parent #4.parent = 5

        if parent == None:
            self.root = node
        elif node.data < parent.data: #5.left = 4
            parent.left = node
        else:
            parent.right = node

        if node.parent == None:
            node.color = "Black"
            return
        
        self.fixInsert(node)
    
    def inorder_traversal(self):
        self.inorder_helper(self.root)
        


if __name__ == '__main__':

    rbtree = RBTree()

    rbtree.insert(4, 'hello')
    rbtree.insert('name', 'ishan')
    # # rbtree.inorder_traversal()
    # rbtree.insert(6)
    # rbtree.insert(15)
    # rbtree.insert(-1)

    rbtree.inorder_traversal()
    print(rbtree.size)