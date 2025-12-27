#id1: 212287205
#name1: Ilia Gorlitsky 
#username1: iliyag
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		if key is not None:
			self.key = key
			self.value = value
			self.left = AVLNode(None, None)
			self.left.parent = self
			self.right = AVLNode(None, None)
			self.right.parent = self
			self.height = 0
		else:
			self.key = None
			self.value = None
			self.height = -1
		
		self.parent = None
	

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return True if self.height != -1 else False 
		


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = AVLNode(None,None)
		self.max_node_pointer = self.root
		self.tree_size = 0
  
	


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""

	def search_rec(self, n, key, e):
		if not n.is_real_node():
			return None, e + 1
		if n.key == key:
			return n, e + 1
		elif key < n.key:
			return self.search_rec(n.left, key, e+1)
		else:
			return self.search_rec(n.right, key, e+1)
     
	def search(self, key):
		# Start searching from the root
		return self.search_rec(self.root, key, 0)

	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		e = 0
		finger = self.max_node_pointer
		
		if not finger.is_real_node():
			return None, 1

		# Case 1 - key is at the finger
		if key == finger.key:
			return finger, 1
		# Case 2 - key is greater than finger's key (INVALID CASE)
		if key > finger.key:
			return None, 2

		# Case 3 - key is less than finger's key. Move up the tree 
  		# until we find a node with key less than or equal to key
		node = finger
		while node.parent is not None and key < node.key:
			node = node.parent
			e += 1
		result_node, additional_edges = self.search_rec(node, key, 0)
		return result_node, e + additional_edges


	def rotate_left(self, a):
		b = a.right               
		b.parent = a.parent
		a.parent = b        
			# update parent's child pointer
		if b.parent is None: # a is originally a root
			self.root = b
		elif a.key < b.parent.key: 
			b.parent.left = b
		else:
			b.parent.right = b
		
		# update child's pointer
		a.right = b.left          
		a.right.parent = a
		b.left = a
		
		# update height field
		a.height = 1 + max(a.left.height, a.right.height)
		b.height = 1 + max(b.left.height, b.right.height)

	def rotate_right(self, a):
		b = a.left
		b.parent = a.parent
		a.parent = b
		
		# update parent's child pointer
		if b.parent is None: # a is originally a root
			self.root = b
		elif a.key < b.parent.key:
			b.parent.left = b
		else:
			b.parent.right = b		
		
		# update child's pointer
		a.left = b.right
		a.left.parent = a
		b.right = a
		
		# update height field
		a.height = 1 + max(a.left.height, a.right.height)
		b.height = 1 + max(b.left.height, b.right.height)


	
	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""

	def insert(self, key, val):
		e = 0
		h = 0
		n = self.root
		x = AVLNode(key, val) 
		
		# case of an empty tree
		if not n.is_real_node(): 
			self.root = x
			self.max_node_pointer = x
			self.tree_size += 1
			return x, 0, 0
		
		# first stage - regular insert
		while n.is_real_node():
			parent = n
			if key < n.key:
				n = n.left
			elif key > n.key:
				n = n.right
			else: # key already exists, just change value
				n.value = val
				return n, e, 0 
			e += 1
		
		# we've found the parent, check if x should be on the right or left side
		x.parent = parent
		if parent.key < key:
			parent.right = x
		else:
			parent.left = x
   
		# update max_node_pointer if needed
		if key > self.max_node_pointer.key:
			self.max_node_pointer = x

		self.tree_size += 1
		# balancing the tree and updating height field of the nodes
		n = x
		while n.parent is not None and n.is_real_node(): # worst case we get to the root -  we want be able to get there
			n = n.parent
			new_height = 1 + max(n.left.height, n.right.height)
			bf = n.left.height - n.right.height
			
			if new_height == n.height:
				return x, e, h
			else:
				n.height = new_height # fix current height 
				h += 1
				
				if bf == -2: # 1st case of imbalance
					right_son = n.right
					bf_right_son = right_son.left.height - right_son.right.height 
					
					if bf_right_son == -1:
						self.rotate_left(n)
						h += 1
					else:
						self.rotate_right(n.right)
						self.rotate_left(n)
						h += 2
					return x, e, h
			
				elif bf == 2: # 2nd case of imbalance
					left_son = n.left
					bf_left_son = left_son.left.height - left_son.right.height
					
					if bf_left_son == 1: 
						self.rotate_right(n)
						h += 1
					else: 
						self.rotate_left(n.left)
						self.rotate_right(n)
						h += 2
					return x, e, h
					
		return x, e, h
					
			


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		new_node = AVLNode(key, val)
		e = 0
		h = 0
		n = self.max_node_pointer
		# --- Case 1: Empty tree ---
		if not n.is_real_node(): 
			self.root = new_node
			self.max_node_pointer = new_node
			self.tree_size += 1
			return new_node, 0, 0

		# --- Case 2: Insert as new max ---
		if key > n.key: 
			n.right = new_node
			new_node.parent = n
			self.max_node_pointer = new_node
			e = 1

		else:
			# --- Case 3: General case ---
			# Move up the tree until we find a node with key less than or equal to key
			while n.parent is not None and key < n.key:
				n = n.parent
				e += 1
	
			# Now perform a regular insert starting from node n
			parent = n
			current = n
			while current.is_real_node():
				parent = current
				if key < current.key:
					current = current.left	
				elif key > current.key:	
					current = current.right
				else: # key already exists, just change value
					current.value = val
					return current, e, 0
				e += 1
	
			# we've found the parent, check if x should be on the right or left side
			new_node.parent = parent			
			if key < parent.key:
				parent.left = new_node
			else:
				parent.right = new_node

		# update max_node_pointer if needed
		if key > self.max_node_pointer.key:
			self.max_node_pointer = new_node

		self.tree_size += 1

		#TODO: Start fixing heights and rebalancing from that node up to the root
		n = new_node
		while n.parent is not None and n.is_real_node(): # worst case we get to the root -  we want be able to get there
			n = n.parent
			new_height = 1 + max(n.left.height, n.right.height)
			bf = n.left.height - n.right.height
			
			if new_height == n.height:
				return new_node, e, h
			else:
				n.height = new_height # fix current height 
				h += 1
				
				if bf == -2: # 1st case of imbalance
					right_son = n.right
					bf_right_son = right_son.left.height - right_son.right.height 
					
					if bf_right_son == -1:
						self.rotate_left(n)
						h += 1
					else:
						self.rotate_right(n.right)
						self.rotate_left(n)
						h += 2
					return new_node, e, h
			
				elif bf == 2: # 2nd case of imbalance
					left_son = n.left
					bf_left_son = left_son.left.height - left_son.right.height
					
					if bf_left_son == 1: 
						self.rotate_right(n)
						h += 1
					else: 
						self.rotate_left(n.left)
						self.rotate_right(n)
						h += 2
					return new_node, e, h
		return new_node, e, h

	def delete(self, node):
		"""
		Deletes a given node from the AVL tree and rebalances.
		"""
		if node is None or not node.is_real_node():
			return

		if node.parent is not None and not node.parent.is_real_node():
			return

		# --- helper: replace u by v in the tree ---
		def transplant(u, v):
			if u.parent is None:
				self.root = v
			elif u == u.parent.left:
				u.parent.left = v
			else:
				u.parent.right = v
			if v is not None:
				v.parent = u.parent

		# --- helper: find minimum in subtree ---
		def subtree_min(n):
			while n.left.is_real_node():
				n = n.left
			return n

		# --- update max_node_pointer if needed ---
		if node == self.max_node_pointer:
			# Find the predecessor (next largest node)
			if node.left.is_real_node():
				# Max in left subtree
				self.max_node_pointer = node.left
				while self.max_node_pointer.right.is_real_node():
					self.max_node_pointer = self.max_node_pointer.right
			elif node.parent is not None:
				# Walk up to find an ancestor where we came from the right
				current = node
				parent = node.parent
				while parent is not None and current == parent.left:
					current = parent
					parent = parent.parent
				self.max_node_pointer = parent if parent is not None else AVLNode(None, None)
			else:
				# Tree becomes empty
				self.max_node_pointer = AVLNode(None, None)

		# --- actual deletion ---
		if not node.left.is_real_node():  # 0 or right-only child
			start_fix = node.parent
			transplant(node, node.right)

		elif not node.right.is_real_node():  # left-only child
			start_fix = node.parent
			transplant(node, node.left)

		else:  # two children
			successor = subtree_min(node.right)

			if successor.parent != node:
				start_fix = successor.parent
				transplant(successor, successor.right)
				successor.right = node.right
				successor.right.parent = successor
			else:
				start_fix = successor

			transplant(node, successor)
			successor.left = node.left
			successor.left.parent = successor
			successor.height = node.height  # Initialize height

		self.tree_size -= 1

		# --- rebalance upwards ---
		n = start_fix
		while n is not None:
			if not n.is_real_node():
				n = n.parent
				continue

			old_height = n.height
			n.height = 1 + max(n.left.height, n.right.height)
			bf = n.left.height - n.right.height

			if bf == 2:
				if n.left.left.height >= n.left.right.height:
					self.rotate_right(n)
				else:
					self.rotate_left(n.left)
					self.rotate_right(n)

			elif bf == -2:
				if n.right.right.height >= n.right.left.height:
					self.rotate_left(n)
				else:
					self.rotate_right(n.right)
					self.rotate_left(n)

			n = n.parent

	def split(self, node):
		# Handle None or invalid input
		if node is None or not isinstance(node, AVLNode) or not node.is_real_node():
			left_tree = AVLTree()
			right_tree = AVLTree()
			return left_tree, right_tree
		
		# Initialize the two resulting trees
		left_tree = AVLTree()
		right_tree = AVLTree()

		# Detach node's children
		if node.left.is_real_node():
			left_tree.root = node.left
			left_tree.root.parent = None
		else:
			left_tree.root = AVLNode(None, None)

		if node.right.is_real_node():
			right_tree.root = node.right
			right_tree.root.parent = None
		else:
			right_tree.root = AVLNode(None, None)

		# Disconnect node completely
		parent = node.parent
		curr = node

		node.left = AVLNode(None, None)
		node.right = AVLNode(None, None)
		node.parent = None

		# Walk upward and join along the path
		while parent is not None:
			if curr == parent.left:
				# parent.key and parent.right belong to RIGHT tree
				temp = AVLTree()
				if parent.right.is_real_node():
					temp.root = parent.right
					temp.root.parent = None
				else:
					temp.root = AVLNode(None, None)

				right_tree.join(
					temp,
					parent.key,
					parent.value
				)

			else:
				# parent.key and parent.left belong to LEFT tree
				temp = AVLTree()
				if parent.left.is_real_node():
					temp.root = parent.left
					temp.root.parent = None
				else:
					temp.root = AVLNode(None, None)

				left_tree.join(
					temp,
					parent.key,
					parent.value
				)

			curr = parent
			parent = parent.parent

		return left_tree, right_tree

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""

	def join(self, tree2, key, val):
			
			# find the tallest tree & who has the smaller values 
			h_self = self.root.height if self.root.is_real_node() else -1
			h_tree2 = tree2.root.height if tree2.root.is_real_node() else -1
			
			T_high = self if h_self > h_tree2 else tree2
			T_low = tree2 if T_high == self else self
			
			# handle empty trees
			if not self.root.is_real_node() and not	tree2.root.is_real_node():
				x = AVLNode(key,val)
				self.root = x
				self.tree_size = 1
				self.max_node_pointer = x
				tree2.root = AVLNode(None, None) # Clear tree2
				tree2.tree_size = 0
				tree2.max_node_pointer = AVLNode(None, None)
				return	
			elif not self.root.is_real_node():
				if tree2.root.key < key:
					T_l = tree2
					T_r = self
				else:
					T_l = self
					T_r = tree2
			elif not tree2.root.is_real_node():
				if self.root.key < key:
					T_l = self
					T_r = tree2
				else:
					T_l = tree2
					T_r = self
			else:
				# both trees are non-empty,
				if self.root.key > key: 
					T_l = tree2
					T_r = self
				else:
					T_l = self
					T_r = tree2
     
			x = AVLNode(key, val)

			# Case 1: The tree with smaller values is the shorter one
			if T_l == T_low: 
				x.left = T_l.root
				if T_l.root.is_real_node():
					T_l.root.parent = x
				
				n = T_high.root
				target_h = T_l.root.height + 1 if T_l.root.is_real_node() else 0
				
				if not n.is_real_node():
					x.right = AVLNode(None, None)
					x.right.parent = x
					self.root = x
				else: 
					# descend to the left side of the high tree
					while n.height > target_h:
						n = n.left
					
					p = n.parent 
					x.right = n 
					n.parent = x
					
					x.parent = p 
					if p is None: # n was the root
						self.root = x
					else:
						p.left = x

			# Case 2: The tree with larger values is the shorter one
			else: 
				x.right = T_r.root
				if T_r.root.is_real_node():
					T_r.root.parent = x
				
				n = T_high.root
				target_h = T_r.root.height + 1 if T_r.root.is_real_node() else 0
				
				if not n.is_real_node():
					x.left = AVLNode(None, None)
					x.left.parent = x
					self.root = x
				else:
					# descend to the right side of the high tree
					while n.height > target_h:
						n = n.right
					
					p = n.parent 
					x.left = n 
					n.parent = x
					if n.is_real_node():
						n.parent = x
					
					x.parent = p
					if p is None: # n was the root
						self.root = x
					else:
						p.right = x

			# Rebalance from x upwards
			n = x
			while n is not None and n.is_real_node():
				n.height = 1 + max(n.left.height, n.right.height)
				bf = n.left.height - n.right.height
				
				if abs(bf) > 1:
					if bf == 2:
						if n.left.left.height >= n.left.right.height:
							self.rotate_right(n)
						else:
							self.rotate_left(n.left)
							self.rotate_right(n)
					elif bf == -2:
						if n.right.right.height >= n.right.left.height:
							self.rotate_left(n)
						else:
							self.rotate_right(n.right)
							self.rotate_left(n)
				
				n = n.parent
			
			# Update tree size
			self.tree_size = self.tree_size + tree2.tree_size + 1 
			
			# Update max_node_pointer
			if T_r.root.is_real_node():
				self.max_node_pointer = T_r.max_node_pointer
			else:
				self.max_node_pointer = x
			
			# Update root pointer
			new_root = x
			while new_root.parent is not None:
				new_root = new_root.parent
			self.root = new_root
	
			tree2.root = AVLNode(None, None) # Clear tree2
			tree2.tree_size = 0
			tree2.max_node_pointer = AVLNode(None, None)
			return 


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
     
		if node is None or not isinstance(node, AVLNode) or not node.is_real_node():
			left_tree = AVLTree()
			right_tree = AVLTree()
			return left_tree, right_tree

		# Initialize the two resulting trees
		left_tree = AVLTree()
		right_tree = AVLTree()

		# Detach node's children
		if node.left.is_real_node():
			left_tree.root = node.left
			left_tree.root.parent = None
		else:
			left_tree.root = AVLNode(None, None)

		if node.right.is_real_node():
			right_tree.root = node.right
			right_tree.root.parent = None
		else:
			right_tree.root = AVLNode(None, None)

		# Disconnect node completely
		parent = node.parent
		curr = node

		node.left = AVLNode(None, None)
		node.right = AVLNode(None, None)
		node.parent = None

		# Walk upward and join along the path
		while parent is not None:
			if curr == parent.left:
				# parent.key and parent.right belong to RIGHT tree
				temp = AVLTree()
				if parent.right.is_real_node():
					temp.root = parent.right
					temp.root.parent = None
				else:
					temp.root = AVLNode(None, None)

				right_tree.join(
					temp,
					parent.key,
					parent.value
				)

			else:
				# parent.key and parent.left belong to LEFT tree
				temp = AVLTree()
				if parent.left.is_real_node():
					temp.root = parent.left
					temp.root.parent = None
				else:
					temp.root = AVLNode(None, None)

				left_tree.join(
					temp,
					parent.key,
					parent.value
				)

			curr = parent
			parent = parent.parent

		return left_tree, right_tree


	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):

		res = []

		def inorder(n):
			if not n.is_real_node():
				return
			inorder(n.left)
			res.append((n.key, n.value))
			inorder(n.right)

		inorder(self.root)
		return res

	
	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""

	def max_node(self):
		return None if not self.max_node_pointer.is_real_node() else self.max_node_pointer


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

	def size(self):	
		return self.tree_size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None if not self.root.is_real_node() else self.root

	def print_tree(self):
		"""Prints the AVL tree sideways (right to left)"""
		def print_node(node, level=0):
			if node.is_real_node():
				print_node(node.right, level + 1)
				print(' ' * 4 * level + '->', node.key)
				print_node(node.left, level + 1)

		print_node(self.root)
