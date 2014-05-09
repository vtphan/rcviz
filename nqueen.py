from rcviz import callgraph, viz

def display(sol):
   for i in range(len(sol)):
      print('-' * sol[i] + 'Q')
   print('\n')

def promising(sol, i, n):
   for j in range(i):
      if sol[i] == sol[j]:
         return False
      if abs(i-j) == abs(sol[i]-sol[j]):
         return False
   return True

@viz
def queen(sol, i, n):
   if promising(sol, i, n):
      if i == n-1:
         display(sol)
         return True
      else:
         for j in range(n):
            sol[i+1] = j
            queen(sol, i+1, n)
   else:
      return False

if __name__ == '__main__':
   n = 4
   queen([0]*n, -1, n)
   callgraph.render("queens.png")
