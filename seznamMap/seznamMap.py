import os

root_path = r'C:\Users\nucic\Desktop\PYTHON\Bliznjice\seznamMap\make'

directory_list = list()
for root, dirs, files in os.walk(root_path, topdown=False):
    for name in dirs:
        # directory_list.append(os.path.join(root, name))
        print(name)
