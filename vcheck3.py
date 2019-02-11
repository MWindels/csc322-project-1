import collections
import parse_tree as pt

if __name__ == '__main__':
	inputs = []
	raw_inputs = input().split(',')
	for ri in raw_inputs:
		if len(ri.lstrip()) > 0:
			inputs.append(ri)
	
	if len(inputs) > 0:
		formula = inputs[-1]
		axioms = inputs[:(len(inputs) - 1)]
		
		full_formula = ''
		if len(axioms) > 0:
			for i, a in enumerate(axioms):
				full_formula += '(' + a + ')'
				if i < len(axioms) - 1:
					full_formula += '&'
			full_formula += '->'
		full_formula += '(' + formula + ')'
		
		try:
			validity, assignments = pt.ParseTree(full_formula).is_valid()
			if validity:
				print('Formula IS valid given the axioms.')
			else:
				assignments_str = ''
				sorted_assignments = collections.OrderedDict(sorted(assignments.items(), key=lambda kv_pair: kv_pair[0]))
				for i, (k, v) in enumerate(sorted_assignments.items()):
					assignments_str += 'A' + str(k) + ' = ' + ('T' if v else 'F')
					if i < len(sorted_assignments) - 1:
						assignments_str += ', '
				print(assignments_str)
		except pt.ParseError as e:
			user_error = False
			for i, f in enumerate(inputs):
				try:
					pt.ParseTree(f)
				except pt.ParseError as e_user:
					print('Formula ' + str(i + 1) + ' was formatted incorrectly: ' + e_user.message)
					user_error = True
					break
			if not user_error:
				print('Formatting error occurred internally.')	#Should never see this, but just in case...
	else:
		print('Must input at least one boolean formula.')
