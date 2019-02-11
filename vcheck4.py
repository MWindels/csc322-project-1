import timeit
import collections
import parse_tree as pt

'''
This function evaluates whether or not the boolean formula represented by a node in a ParseTree
is true or not given a set of bindings.

Parameters
----------
tree : Disjunction, Conjunction, Negation, or Variable.
	The ParseTree node to evaluate.

bindings : dictionary
	A dictionary that maps the integer ID of every variable in a ParseTree to a true or false value.

Returns
-------
satisfiability : boolean
	Whether or not the set of bindings satisfies the formula at the node.
'''
def __eval_node(node, bindings):
	if type(node) == pt.Disjunction:
		return __eval_node(node.left, bindings) or __eval_node(node.right, bindings)
	elif type(node) == pt.Conjunction:
		return __eval_node(node.left, bindings) and __eval_node(node.right, bindings)
	elif type(node) == pt.Negation:
		return not __eval_node(node.expression, bindings)
	elif type(node) == pt.Variable:
		return bindings[node.original_id()]

'''
This function tests the validity of a boolean formula by brute-force.

Parameters
----------
tree : ParseTree
	The ParseTree representing the boolean formula.

Returns
-------
validity : boolean
	Whether or not the formula in the tree ParseTree is valid.
'''
def brute_force_validity(tree):
	assignments = {k: False for k in tree.used_variables()}
	if len(assignments) > 0:
		for a_permute in range(2 ** len(assignments)):
			for i, var in enumerate(assignments.keys()):
				assignments[var] = True if (a_permute & (2 ** i)) != 0 else False
			if not __eval_node(tree.root, assignments):
				return False
	return True

if __name__ == '__main__':
	formula_str = input()
	if len(formula_str.lstrip()) > 0:
		try:
			formula_tree = pt.ParseTree(formula_str)
			
			brute_valid = brute_force_validity(formula_tree)
			assert(brute_valid == formula_tree.is_valid()[0])
			
			brute_timer = timeit.Timer(lambda: brute_force_validity(formula_tree))
			ncnf_timer = timeit.Timer(lambda: formula_tree.is_valid())
			
			if brute_valid:
				print('Formula IS valid.')
			else:
				print('Formula IS NOT valid.')
			print('Time taken to find validity by:')
			print('\tBrute Force: ' + str(brute_timer.timeit(1)) + ' seconds.')
			print('\tNCNF Conversion: ' + str(ncnf_timer.timeit(1)) + ' seconds.')
		except pt.ParseError as e:
			print('Incorrectly formatted formula: ' + e.message)
	else:
		print('Must input one boolean formula.')
