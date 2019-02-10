import parse_tree as pt

if __name__ == '__main__':
	formula_str = input()
	if len(formula_str.lstrip()) > 0:
		try:
			if pt.ParseTree(formula_str).is_valid()[0]:
				print('Formula IS valid.')
			else:
				print('Formula IS NOT valid.')
		except pt.ParseError as e:
			print('Incorrectly formatted formula: ' + e.message)
	else:
		print('Must input one boolean formula.')
