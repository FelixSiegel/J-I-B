import os
def getListOfFiles(dirName="./",ignored_dirs=[".git",".idea"]):
    listOfFile = os.listdir(dirName)
    allFiles = []
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    all_wanted_files = []
    # check if file is in an ignored dir:
    for file in allFiles:
        for dir in ignored_dirs:
            if dir in file:
                print(file)
                continue
            else:
                all_wanted_files.append(file)
    return all_wanted_files
print(getListOfFiles())
