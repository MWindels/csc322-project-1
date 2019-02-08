import sys
import argparse
import parse_tree as pt

'''
This function returns the formula input as a command line argument.

Parameters
----------
args : list
	The command line arguments, excluding the first one.

Returns
-------
formula : string
	The boolean formula input to the command line.
'''
def get_formula(args):
	parser = argparse.ArgumentParser(description='Check the validity of a boolean formula.')
	parser.add_argument('formula', type=str, help='the boolean formula to check (in quotation marks if spaces and parentheses are involved)')
	return parser.parse_args(args).formula

if __name__ == '__main__':
	try:
		if pt.ParseTree(get_formula(sys.argv[1:])).is_valid():
			print('Formula IS valid.')
		else:
			print('Formula IS NOT valid.')
	except pt.ParseError as e:
		print('Incorrectly formatted formula: ' + e.message)
	except IOError as e:
		print(e.message)
