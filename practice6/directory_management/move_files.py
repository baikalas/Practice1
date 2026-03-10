import shutil

source = "example.txt"
destination = "test_directory/example.txt"

shutil.move(source, destination)

print("File moved to test_directory.")