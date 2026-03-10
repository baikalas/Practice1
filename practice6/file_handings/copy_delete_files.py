import shutil
import os

source = "example.txt"
destination = "copy_example.txt"


shutil.copy(source, destination)
print("File copied.")
os.remove(destination)
print("Copied file deleted.")