import collections
import parse_tree as pt

if __name__ == '__main__':
	formula_str = input()
	if len(formula_str.lstrip()) > 0:
		try:
			value, assign = pt.ParseTree(formula_str).is_valid()
			if value:
				print('Formula IS valid.')
			else:
				sorted_assign = collections.OrderedDict(sorted(assign.items(), key=lambda kv_pair: kv_pair[0]))
				for x in sorted_assign:
					sorted_assign[x] = 'T' if sorted_assign[x] else 'F'
				#Modified from https://codereview.stackexchange.com/questions/7953/flattening-a-dictionary-into-a-string
				print(', '.join("A{!s} = {!s}".format(key,val) for (key,val) in sorted_assign.items()))
		except pt.ParseError as e:
			print('Incorrectly formatted formula: ' + e.message)
	else:
		print('Must input one boolean formula.')
