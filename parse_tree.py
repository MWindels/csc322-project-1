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
				raise ParseError('Invalid token encountered after: \'' + self.__tokens[-1] + '\'.')
			else:
				raise ParseError('Invalid token at beginning of formula.')
		elif len(self.__tokens) > 0:
			self.root = self.__implication()
			if len(self.__tokens) > 0:
				raise ParseError('Unparsed parentheses in formula.')
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
	'''
	def __atom(self):
		token, t_valid = self.__next_token(consume=True)
		if t_valid:
			if token[0] == 'x':
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
				raise ParseError('Unexpected token ' + token + '.')
		else:
			raise ParseError('No token to parse.')

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
	
	def __init__(self, c):
		self.clause = c
	
	def __str__(self):
		return '~' + str(self.clause)

'''
This object represents a variable node (a leaf) in a ParseTree.
'''
class Variable:
	
	def __init__(self, v_id):
		self.var_id = v_id
	
	def __str__(self):
		return 'x' + str(self.var_id)
