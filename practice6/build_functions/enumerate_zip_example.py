names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

# enumerate example
for index, name in enumerate(names):
    print(index, name)

# zip example
for name, score in zip(names, scores):
    print(name, score)