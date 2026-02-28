def squares(n):
    for i in range(n):
        yield i * i
n = int(input())
for square in squares(n):
    print(square)
    