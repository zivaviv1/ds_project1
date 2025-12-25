# import unittest
from AVLTree import AVLTree, AVLNode


tree = AVLTree()
x = tree.insert(10, 'a')
tree.insert(20, 'b')
tree.insert(5, 'c')
tree.insert(15, 'd')
tree.insert(25, 'e')
tree.insert(30, 'f')
tree.insert(3, 'g')
tree.insert(7, 'h')
tree.insert(12, 'i')
tree.insert(17, 'j')
tree.insert(22, 'k')
trees = tree.split(10)
trees[0].print_tree()
trees[1].print_tree()
tree.join(trees[0], x, 'x')
tree.print_tree()
# class TestAVLTree(unittest.TestCase):
#     def test_empty_tree_properties(self):
#         t = AVLTree()
#         self.assertIsNone(t.get_root())
#         self.assertEqual(t.size(), 0)
#         self.assertIsNone(t.max_node())

#     def test_insert_empty_tree(self):
#         t = AVLTree()
#         node, e, h = t.insert(10, 'a')
#         self.assertIsInstance(node, AVLNode)
#         self.assertEqual(node.key, 10)
#         self.assertEqual(node.value, 'a')
#         self.assertEqual(e, 0)
#         self.assertEqual(h, 0)
#         self.assertIsNotNone(t.get_root())
#         self.assertEqual(t.size(), 1)
#         self.assertEqual(t.max_node().key, 10)

#     def test_insert_duplicate_updates_value(self):
#         t = AVLTree()
#         node, e, h = t.insert(5, 'first')
#         self.assertEqual(node.value, 'first')
#         node2, e2, h2 = t.insert(5, 'second')
#         # inserting duplicate should return the existing node and update its value
#         self.assertIs(node, node2)
#         self.assertEqual(node2.value, 'second')
#         self.assertEqual(e2, 0)
#         self.assertEqual(h2, 0)

#     def test_inserts_cause_rotation(self):
#         # inserting in ascending order should rebalance to have middle value as root
#         t = AVLTree()
#         t.insert(1, 'a')
#         t.insert(2, 'b')
#         t.insert(3, 'c')
#         root = t.get_root()
#         # current implementation performs rotations on imbalance; expect root to be 2
#         self.assertIsNotNone(root)
#         self.assertEqual(t.size(), 3)
#         self.assertEqual(root.key, 2)
#         self.assertEqual(t.max_node().key, 3)

#     def test_placeholders_and_unimplemented_methods(self):
#         t = AVLTree()
#         # search / finger_search currently return placeholders
#         s_res = t.search(100)
#         self.assertIsInstance(s_res, tuple)
#         self.assertEqual(s_res, (None, -1))

#         f_res = t.finger_search(100)
#         self.assertIsInstance(f_res, tuple)
#         self.assertEqual(f_res, (None, -1))

#         fi_res = t.finger_insert(1, 'x')
#         self.assertIsInstance(fi_res, tuple)
#         self.assertEqual(fi_res, (None, -1, -1))

#         # delete / join / split / avl_to_array are placeholders
#         self.assertIsNone(t.delete(None))
#         self.assertIsNone(t.join(None, 0, 'v'))
#         self.assertEqual(t.split(None), (None, None))
#         self.assertIsNone(t.avl_to_array())


# def print_tree(self):
# 	"""Prints the AVL tree sideways (right to left)"""

# 	def _print(node, level):
# 		if not node.is_real_node():
# 			return
# 		_print(node.right, level + 1)
# 		print("    " * level + f"{node.key}(h={node.height})")
# 		_print(node.left, level + 1)

# 	_print(self.root, 0)

# if __name__ == '__main__':
#     unittest.main()
