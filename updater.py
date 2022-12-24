import requests
import zipfile
import os
from shutil import copyfile,rmtree
url = "https://github.com/FelixSiegel/J-I-B/archive/refs/heads/main.zip"
download_path = "./temp/bot.zip"
def _download():
    with open(download_path,"wb") as download_file:
        file_content = requests.get(url).content
        download_file.write(file_content)
def _extract_files():
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall("./temp")
def _replace_feature_files(output=True):
    old_files = os.listdir(("./features"))

    for file in old_files:
        if output:
            print(f"Deleting old feature file: {file}")
        os.remove(f"./features/{file}")

    new_files = os.listdir("./temp/J-I-B-main/features")

    for file in new_files:
        file_path = "./temp/J-I-B-main/features/" + file
        if output:
            print(f"Copying new feature:{file}")
        copyfile(file_path,f"./features/{file}")
def _delete_unused_files(output=True):
    if output:
        print("Deleting unused files")
    temp = './temp'
    for filename in os.listdir(temp):
        file_path = os.path.join(temp, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            if output:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


def update(output=True):
    _download()
    _extract_files()
    _replace_feature_files(output=output)
    _delete_unused_files(output=output)
if __name__ == '__main__':
    update()