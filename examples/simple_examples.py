from rcviz import callgraph, viz

Table = {}

@viz
def fib2(n):
	if n not in Table:
		if n<2:
			Table[n] = n
		else:
			Table[n] = fib2(n-1) + fib2(n-2)
	return Table[n] 

@viz
def fib(n):
	if n<2:
		return n
	else:
		return fib(n-1) + fib(n-2)

@viz
def fact(n):
	if n==0: return 1
	return n * fact(n-1)

fib(11)
callgraph.render()
