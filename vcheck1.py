import parse_tree as pt

if __name__ == '__main__':
	print('Input a boolean formula:\n')
	try:
		if pt.ParseTree(input()).is_valid():
			print('Formula IS valid.')
		else:
			print('Formula IS NOT valid.')
	except pt.ParseError as e:
		print('Incorrectly formatted formula: ' + e.message)
	except IOError as e:
		print(e.message)
