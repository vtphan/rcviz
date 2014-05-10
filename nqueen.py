'''
Author: Vinhthuy Phan, 2014
'''
from rcviz import callgraph, viz

N=4


def promising(sol, i):
   for j in range(i):
      if sol[i] == sol[j]:
         return False
      if abs(i-j) == abs(sol[i]-sol[j]):
         return False
   return True

# Enumerate all feasible solutions.  Return color of all found solutions.
@viz
def Queen(sol, i):
   if promising(sol, i):
      if i == N-1:
         return ['bisque']
      else:
         for j in range(N):
            sol[i+1] = j
            Queen(sol, i+1)
   return ['lightgrey']



# Return True if a solution is found.  Annotate with a color.
@viz
def queen(sol, i):
   if promising(sol,i):
      if i == N-1:
         return [True, 'cyan']
      else:
         for j in range(N):
            sol[i+1] = j
            found, _ = queen(sol, i+1)
            if found:
               return [found, 'lightgrey']

   return [False, 'lightgrey']

if __name__ == '__main__':
   # Queen([-1]*N, -1)
   # callgraph.render("queens.png", annotate=True)
   queen([-1]*N, -1)
   callgraph.render("queens.png",annotate=True)
