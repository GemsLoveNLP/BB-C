import numpy as np

def draw(l):
    size = len(l)
    s = ""
    s+="-"*(4*size+1)
    s+="\n"
    for i in range(size):
        s+="|"
        for j in range(size):
            s+=" "
            s+=str(l[i][j])
            s+=" |"
        s+="\n"
        s+="-"*(4*size+1)
        s+="\n"
    return s

l = [[1,2,3],[3,4,5],[4,8,7]]

print(draw(l))

print(np.array(l))