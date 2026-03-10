import os

# Create directory
dir_name = "test_directory"
os.makedirs(dir_name, exist_ok=True)

print("Directory created.")

# List directories and files
items = os.listdir(".")
print("Current directory contents:")

for item in items:
    print(item)