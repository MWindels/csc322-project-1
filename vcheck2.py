import parse_tree as pt

if __name__ == '__main__':
	print('Input a boolean formula:\n')
	try:
		value, assign = pt.ParseTree(input()).is_valid()
		if value:
			print('Formula IS valid.')
		else:
			for x in assign:
				assign[x] = 'T' if assign[x] else 'F'
			#Modified from https://codereview.stackexchange.com/questions/7953/flattening-a-dictionary-into-a-string
			print(', '.join("A{!s} = {!s}".format(key,val) for (key,val) in assign.items()))
	except pt.ParseError as e:
		print('Incorrectly formatted formula: ' + e.message)
