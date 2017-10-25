from rcviz import callgraph, viz
import copy

def merge(y, z):
    result = []
    while (len(y) > 0) and (len(z) > 0):
        if y[0] > z[0]:
            result.append(z.pop(0))
        else:
            result.append(y.pop(0))
    return result + y + z

@viz
def msort(x):
    if len(x) < 2:
        return x
    mid = int(len(x)/2)
    y = msort(x[:mid])
    z = msort(x[mid:])
    return merge(y,z)

msort([4,8,3,10,5,1,2,15,7,6])
# callgraph.render("ms.png")
