import re

'''
Tokenizes a boolean formula expressed as a string.

The valid tokens are paraentheses, negation (~), conjunction (&), disjunction (v), material
implication (->), and variables (x[1-9][0-9]*).  All whitespace is ignored.

Parameters
----------
formula_str : string
	A boolean formula expressed as a string.

Returns
-------
tokens : list
	A list of tokens (strings) successfully derived from formula_str.

valid : boolean
	Whether or not the whole boolean formula was successfully tokenized.

'''
def tokenize(formula_str):
	tokens = []
	working_str = formula_str.lstrip()
	while(len(working_str) > 0):
		next_ch = working_str[0]
		if next_ch == '(' or next_ch == ')' or next_ch == '~' or next_ch == '&' or next_ch == 'v':
			tokens.append(next_ch)
			working_str = working_str[1:]
		elif len(working_str) > 1:
			if next_ch == '-' and working_str[1] == '>':
				tokens.append('->')
				working_str = working_str[2:]
			elif next_ch == 'x':
				var_num = re.match('[1-9][0-9]*', working_str[1:])	# Note that match(...) checks at the beginning of the string.
				if var_num is not None:
					tokens.append('x' + var_num.group())
					working_str = working_str[(1 + var_num.span()[1]):]
				else:
					return tokens, False
			else:
				return tokens, False
		else:
			return tokens, False
		
		working_str = working_str.lstrip()
	
	return tokens, True
