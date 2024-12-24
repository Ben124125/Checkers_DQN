import numpy as np
import torch

l = [[(1,2),(3,4)], [(5,6),(7,8)], [(9,10),(11,12)]]

t = torch.tensor(l).reshape(-1, 4)
print(t.shape)
print(t)

print("hi",end="\r")

p = [True,False,False,True]

o = torch.tensor(p)
print(o)

x = (1,2)
y = (1,2)

if x == y:
    print('true')

gh = [(1,2)]

if gh != []:
    print('gsa')

