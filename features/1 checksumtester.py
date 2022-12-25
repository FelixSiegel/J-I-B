import os
from hashlib import sha512
import requests
def _search(folder_path: str = "./", ignored_dirs: list = [".git",".idea"]):# thx ice :D
    file_list = []
    for path, subdirs, files in os.walk(folder_path, topdown=True):
        if not any(ignore in path for ignore in ignored_dirs):
            for file in files:
                file_list.append(os.path.join(path, file))

    return file_list

def get_sum(files):
    sums = []
    for file in files:
        with open(file,"r") as opened_file:
            content = opened_file.read()
            hash = sha512(content.encode())
            sum = hash.hexdigest()
            #print(f"{file} : {sum}\n")
            sums.append(sum)

    project_sum = ""
    for sum in sums:
        project_sum = project_sum + sum
    #print(project_sum)
    return project_sum
def compare_sum(sum):
    original_sum = requests.get("https://raw.githubusercontent.com/FelixSiegel/J-I-B/main/checksum.txt").text
    print(original_sum+"\n"+sum)
    if sum == original_sum:
        return True
    else:
        return False
print(compare_sum(get_sum(_search())))