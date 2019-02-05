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
			return Disjunction(Negation(left), self.__implication())
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
			return Disjunction(left, self.__disjunction())
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
			return Conjunction(left, self.__conjunction())
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
					self.__replace_parent(Conjunction(Negation(non_negation.left), Negation(non_negation.right)), current[1], current[2])
				elif type(non_negation) == Conjunction:
					self.__replace_parent(Disjunction(Negation(non_negation.left), Negation(non_negation.right)), current[1], current[2])
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
This object represents a disjunction (internal) node in a ParseTree.
'''
class Disjunction:
	
	def __init__(self, l, r):
		self.left = l
		self.right = r
	
	def __str__(self):
		return '(' + str(self.left) + ' v ' + str(self.right) + ')'

'''
This object represents a conjunction node (internal) in a ParseTree.
'''
class Conjunction:
	
	def __init__(self, l, r):
		self.left = l
		self.right = r
	
	def __str__(self):
		return '(' + str(self.left) + ' & ' + str(self.right) + ')'

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
		self.var_id = v_id
	
	def __str__(self):
		return 'A' + str(self.var_id)
