import parse_tree as pt

if __name__ == '__main__':
	try:
		print('Input a boolean formula:\n')
		formula = input()
		
		axioms = []
		print('Input 0 or more axioms:\n')
		axioms.append(input())
		while axioms[-1].lstrip() != '':
			axioms.append(input())
		
		axioms = axioms[:(len(axioms) - 1)]
		total_formula = ''
		if len(axioms) > 0:
			for i, a in enumerate(axioms):
				total_formula += '(' + a + ')'
				if i < len(axioms) - 1:
					total_formula += '&'
			total_formula += '->'
		total_formula += '(' + formula + ')'
		
		if pt.ParseTree(total_formula).is_valid():
			print('Formula IS valid given the axioms.')
		else:
			print('Formula IS NOT valid given the axioms.')
	except pt.ParseError as e:
		print('Incorrectly formatted formula: ' + e.message)
	except IOError as e:
		print(e.message)
