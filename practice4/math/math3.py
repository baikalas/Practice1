from math import tan

a,b = map(float, input().split())
s = (a * (b **2)) / (4 * tan(3.14/a))
print(s)