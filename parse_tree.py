import tokenizer as tok

'''
This object is an exception type raised by the ParseTree while parsing.
'''
class ParseError(Exception):
	
	def __init__(self, m):
		self.message = m
	
	def __str__(self):
		return repr(self.message)

'''
This object is an abstract syntax tree which parses a boolean expression.  The supported
connectives and variable names are the same as those supported by tokenizer.tokenize().  This
object is essentially a recursive descent parser.
'''
class ParseTree:
	
	'''
	Initializes a new ParseTree.
	
	Parameters
	----------
	formula : string
		A boolean formula as a string.
	
	Raises
	------
	ParseError
		If an error occurs while parsing the formula.
	'''
	def __init__(self, formula):
		self.__connective_count = 0
		self.__tokens, valid = tok.tokenize(formula)
		if not valid:
			if len(self.__tokens) > 0:
				raise ParseError('Invalid token encountered after: \"' + self.__tokens[-1] + '\".')
			else:
				raise ParseError('Invalid token at beginning of formula.')
		elif len(self.__tokens) > 0:
			self.root = self.__implication()
			if len(self.__tokens) > 0:
				raise ParseError('Unparsed tokens in formula.')
		else:
			self.root = None
	
	'''
	Converts the ParseTree to a string.
	'''
	def __str__(self):
		return str(self.root)
	
	'''
	Pre-increments __connective_count because Python doesn't support unary ++.
	
	Returns
	-------
	__connective_count : int
		The value of __connective_count after incrementing.
	'''
	def __inc_cc(self):
		self.__connective_count += 1
		return self.__connective_count
	
	'''
	Returns the next token to be parsed.
	
	Parameters
	----------
	consume : boolean
		Whether or not to consume the next token.
	
	Returns
	-------
	token : string
		The next token.
	
	valid : boolean
		Whether or not the token returned is valid.
	'''
	def __next_token(self, consume=False):
		if len(self.__tokens) > 0:
			token = self.__tokens[0]
			if consume:
				self.__tokens.pop(0)
			return token, True
		else:
			return '', False
	
	'''
	This function parses an implication.
	
	Returns
	-------
	Some ParseTree node representing a variable or connective.
	
	Raises
	------
	ParseError
		If an error occurs while parsing the expression.
	'''
	def __implication(self):
		left = self.__disjunction()
		token, t_valid = self.__next_token()
		if t_valid and token == '->':
			self.__next_token(consume=True)
			return Disjunction(self.__inc_cc(), Negation(left), self.__implication())
		else:
			return left
	
	'''
	This function parses a disjunction.
	
	See __implication for return values and exceptions raised.
	'''
	def __disjunction(self):
		left = self.__conjunction()
		token, t_valid = self.__next_token()
		if t_valid and token == 'v':
			self.__next_token(consume=True)
			return Disjunction(self.__inc_cc(), left, self.__disjunction())
		else:
			return left
	
	'''
	This function parses a conjunction.
	
	See __implication for return values and exceptions raised.
	'''
	def __conjunction(self):
		left = self.__negation()
		token, t_valid = self.__next_token()
		if t_valid and token == '&':
			self.__next_token(consume=True)
			return Conjunction(self.__inc_cc(), left, self.__conjunction())
		else:
			return left
	
	'''
	This function parses a negation.
	
	See __implication for return values and exceptions raised.
	'''
	def __negation(self):
		token, t_valid = self.__next_token()
		if t_valid and token == '~':
			self.__next_token(consume=True)
			return Negation(self.__negation())
		else:
			return self.__atom()
	
	'''
	This function parses a variable or parenthesized expression.
	
	See __implication for return values and exceptions raised.
	'''
	def __atom(self):
		token, t_valid = self.__next_token(consume=True)
		if t_valid:
			if token[0] == 'A':
				return Variable(int(token[1:]))
			elif token == '(':
				expr = self.__implication()
				right_paren, rp_valid = self.__next_token()
				if rp_valid and right_paren == ')':
					self.__next_token(consume=True)
					return expr
				else:
					raise ParseError('Non-matching parentheses.')
			else:
				raise ParseError('Unexpected token \"' + token + '\".')
		else:
			raise ParseError('No token to parse.')
	
	'''
	This function replaces the parent of a node.
	
	Parameters
	----------
	node : Disjunction, Conjunction, Negation, or Variable
		The node whose parent is being changed.
	
	new_parent : Disjunction, Conjunction, Negation, or None
		The new parent node (if None, then the node will become self.root).
	
	left_child : boolean
		Whether or not to replace the left child of the parent instead of the right (if it has one).
	'''
	def __replace_parent(self, node, new_parent=None, left_child=True):
		if new_parent is not None:
			if type(new_parent) == Disjunction or type(new_parent) == Conjunction:
				if left_child:
					new_parent.left = node
				else:
					new_parent.right = node
			elif type(new_parent) == Negation:
				new_parent.expression = node
		else:
			self.root = node
	
	'''
	This function counts the number of negations starting at a particular node.
	
	Parameters
	----------
	first_node : Disjunction, Conjunction, Negation, or Variable
		The node to start counting from.
	
	Returns
	-------
	negations : int
		The number of negations encountered.
	
	final_node : Disjunction, Conjunction, or Variable
		The first non-negation node.
	'''
	def __count_negations(self, first_node):
		negations = 0
		final_node = first_node
		while type(final_node) == Negation:
			final_node = final_node.expression
			negations += 1
		return negations, final_node
	
	'''
	This function descends the ParseTree, applies De Morgan's laws, and simplifies double negations.
	
	This has the effect of pushing all negations down to the variables.
	'''
	def literalize(self):
		stack = [(self.root, None, True)]	#Tuple details: (node, parent, node-is-left-child).
		while len(stack) > 0:
			current = stack.pop()
			n_count, non_negation = self.__count_negations(current[0])
			if n_count % 2 == 0:
				self.__replace_parent(non_negation, current[1], current[2])
			else:
				if type(non_negation) == Disjunction:
					self.__replace_parent(Conjunction(non_negation.original_id(), Negation(non_negation.left), Negation(non_negation.right)), current[1], current[2])
				elif type(non_negation) == Conjunction:
					self.__replace_parent(Disjunction(non_negation.original_id(), Negation(non_negation.left), Negation(non_negation.right)), current[1], current[2])
				else:
					self.__replace_parent(non_negation, current[0])
			
			if type(non_negation) == Disjunction or type(non_negation) == Conjunction:
				if current[1] is not None:
					if current[2]:
						stack.extend([(current[1].left.left, current[1].left, True), (current[1].left.right, current[1].left, False)])
					else:
						stack.extend([(current[1].right.left, current[1].right, True), (current[1].right.right, current[1].right, False)])
				else:
					stack.extend([(self.root.left, self.root, True), (self.root.right, self.root, False)])
	
	'''
	This function returns a new ParseTree which is the negation of the current ParseTree in CNF form.
	A polynomial time algorithm is used to convert to CNF.  Also literalizes() the current ParseTree.
	
	Returns
	-------
	new_tree : ParseTree
		A new ParseTree in CNF form corresponding to the negation of the original.
	'''
	def poly_ncnf(self):
		new_tree = ParseTree('')	#Creates an empty tree.
		if self.root is not None:
			proper_root = self.__count_negations(self.root)[1]
			new_tree.root = Negation(Variable(proper_root.original_id())) if type(proper_root) != Variable else Negation(Variable(self.__connective_count + proper_root.original_id()))	#This variable represents ~A_all.
			self.literalize()
			
			stack = [self.root]
			while len(stack) > 0:
				current = stack.pop()
				if type(current) == Disjunction or type(current) == Conjunction:
					x_current = Variable(current.original_id())
					
					ln_count, left = self.__count_negations(current.left)
					x_left = Variable(left.original_id()) if type(left) != Variable else Variable(self.__connective_count + left.original_id())
					if ln_count % 2 == 1:
						x_left = Negation(x_left)
					
					rn_count, right = self.__count_negations(current.right)
					x_right = Variable(right.original_id()) if type(right) != Variable else Variable(self.__connective_count + right.original_id())
					if rn_count % 2 == 1:
						x_right = Negation(x_right)
					
					if type(current) == Disjunction:
						clause_1 = Disjunction(new_tree.__inc_cc(), Negation(x_current), Disjunction(new_tree.__inc_cc(), x_left, x_right))	#False & False -> False
						clause_2 = Disjunction(new_tree.__inc_cc(), x_current, Disjunction(new_tree.__inc_cc(), x_left, Negation(x_right)))	#False & True -> True
						clause_3 = Disjunction(new_tree.__inc_cc(), x_current, Disjunction(new_tree.__inc_cc(), Negation(x_left), x_right))	#True & False -> True
						clause_4 = Disjunction(new_tree.__inc_cc(), x_current, Disjunction(new_tree.__inc_cc(), Negation(x_left), Negation(x_right)))	#True / True -> True
						new_tree.root = Conjunction(new_tree.__inc_cc(), clause_1, Conjunction(new_tree.__inc_cc(), clause_2, Conjunction(new_tree.__inc_cc(), clause_3, Conjunction(new_tree.__inc_cc(), clause_4, new_tree.root))))
					else:	#Implicity means current is a Conjunction.
						clause_1 = Disjunction(new_tree.__inc_cc(), Negation(x_current), Disjunction(new_tree.__inc_cc(), x_left, x_right))	#False & False -> False
						clause_2 = Disjunction(new_tree.__inc_cc(), Negation(x_current), Disjunction(new_tree.__inc_cc(), x_left, Negation(x_right)))	#False & True -> False
						clause_3 = Disjunction(new_tree.__inc_cc(), Negation(x_current), Disjunction(new_tree.__inc_cc(), Negation(x_left), x_right))	#True & False -> False
						clause_4 = Disjunction(new_tree.__inc_cc(), x_current, Disjunction(new_tree.__inc_cc(), Negation(x_left), Negation(x_right)))	#True & True -> True
						new_tree.root = Conjunction(new_tree.__inc_cc(), clause_1, Conjunction(new_tree.__inc_cc(), clause_2, Conjunction(new_tree.__inc_cc(), clause_3, Conjunction(new_tree.__inc_cc(), clause_4, new_tree.root))))
					
					if type(left) == Disjunction or type(left) == Conjunction:
						stack.append(left)
					
					if type(right) == Disjunction or type(right) == Conjunction:
						stack.append(right)
		
		new_tree.literalize()	#Used for simplifying the double negations that might appear on some variables.
		return new_tree
		

'''
This object represents a disjunction node (internal) in a ParseTree.
'''
class Disjunction:
	
	def __init__(self, c_id, l, r):
		self.connective_id = 2 * c_id + 1
		self.left = l
		self.right = r
	
	def __str__(self):
		return '(' + str(self.left) + ' v ' + str(self.right) + ')'
	
	def original_id(self):
		return (self.connective_id - 1) // 2

'''
This object represents a conjunction node (internal) in a ParseTree.
'''
class Conjunction:
	
	def __init__(self, c_id, l, r):
		self.connective_id = 2 * c_id + 1
		self.left = l
		self.right = r
	
	def __str__(self):
		return '(' + str(self.left) + ' & ' + str(self.right) + ')'
	
	def original_id(self):
		return (self.connective_id - 1) // 2

'''
This object represents a negation node (internal) in a ParseTree.
'''
class Negation:
	
	def __init__(self, e):
		self.expression = e
	
	def __str__(self):
		return '~' + str(self.expression)

'''
This object represents a variable node (a leaf) in a ParseTree.
'''
class Variable:
	
	def __init__(self, v_id):
		self.var_id = 2 * v_id
	
	def __str__(self):
		return 'A' + str(self.var_id // 2)
	
	def original_id(self):
		return self.var_id // 2
