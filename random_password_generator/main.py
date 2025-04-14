import random as rd
a = "abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
n=5
for i in range(0,n):
    print(rd.choice(a),end="")