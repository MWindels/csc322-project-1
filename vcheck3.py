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
		
		validity, assignments = pt.ParseTree(total_formula).is_valid()
		if validity:
			print('Formula IS valid given the axioms.')
		else:
			print('Formula IS NOT valid given the axioms.')
			assignments_str = 'Assignment of the variables which shows invalidity: '
			for k, v in assignments.items():
				assignments_str += 'A' + str(k) + ' = ' + str(v) + ', '
			print(assignments_str[:(len(assignments_str) - 2)])
	except pt.ParseError as e:
		print('Incorrectly formatted formula: ' + e.message)
