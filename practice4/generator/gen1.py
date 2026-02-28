def num(n):
    for i in range(n):
        yield i * i

n = int(input())  
for square in num(n):
    print(square)