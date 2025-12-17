#id1: 212287205
#name1: Ilia Gorlitsky 
#username1:iliyag
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
			return None, e
		if n.key == key:
			return n, e
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
		# Case 1 - key is at the finger
		if key == finger.key:
			return finger, e
		# Case 2 - key is greater than finger's key (INVALID CASE)
		if key > finger.key:
			return None, e + 1

		# Case 3 - key is less than finger's key. Move up the tree 
  		# until we find a node with key less than or equal to key
		node = finger
		while node.parent is not None and key < node.key:
			node = node.parent
			e += 1
		return self.search_rec(node, key, e)
		
		
			


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


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
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
			
			# determine which tree has smaller keys 
			if self.root.is_real_node() and self.root.key > key:
				T_r = self
				T_l = tree2
			else:
				T_r = tree2
				T_l = self

			x = AVLNode(key, val)

			# Case 1: The tree with smaller values is the shorter one
			if T_l == T_low: 
				x.left = T_l.root
				T_l.root.parent = x
				
				n = T_high.root
				target_h = T_l.root.height + 1 if T_l.root.is_real_node() else 0
				
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
				T_r.root.parent = x
				
				n = T_high.root
				target_h = T_r.root.height + 1 if T_r.root.is_real_node() else 0
				
				# descend to the right side of the high tree
				while n.height > target_h:
					n = n.right
				
				p = n.parent 
				x.left = n 
				n.parent = x
				
				x.parent = p
				if p is None: # n was the root
					self.root = x
				else:
					p.right = x

			# Ensure self.root points to the correct new root if tree2 was taller
			if T_high == tree2 and self.root != x:
				self.root = tree2.root
				
			tree2.root = AVLNode(None, None) # Clear tree2

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
		return None, None

	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	# [ZIV] changed to use self.max_node_pointer
	def max_node(self):
		return None if not self.max_node_pointer.is_real_node() else self.max_node_pointer
		# n = self.root
		# if not n.is_real_node():
		# 	return None
		# while n.right.is_real_node():
		# 	n = n.right
		# return n


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
 # [ZIV] changed to use self.tree_size
	def size(self):	
		return self.tree_size
		# def size_rec(n):
		# 	if not n.is_real_node():
		# 		return 0
		# 	return 1 + size_rec(n.left) + size_rec(n.right)
		
		# return size_rec(self.root)	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return None if not self.root.is_real_node() else self.root

