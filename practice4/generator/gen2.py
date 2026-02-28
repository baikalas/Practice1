def num(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i

n = int(input())
for even in num(n):
    print(even)