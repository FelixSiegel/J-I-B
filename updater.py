import requests
import zipfile
import os
import json
from shutil import copyfile, rmtree

code_url = "https://github.com/FelixSiegel/J-I-B/archive/refs/heads/main.zip"
version_url = "https://raw.githubusercontent.com/FelixSiegel/J-I-B/main/client_info.json"
download_path = "./temp/bot.zip"


def _check_update():
    # first get version-number of git remote
    content_str = requests.get(version_url).text
    content = json.loads(content_str)
    remote_ver = content["version"]

    # compare local version-number with git remote
    with open("./.client_info.json") as fo:
        local_ver = json.load(fo)["version"]
        # if no new version -> it's not necessary to update
        if local_ver == remote_ver:
            print("\n\033[92m[INFO]:\033[00m No updates available!\n")
            return False
        else:
            return True


def _download():
    with open(download_path, "wb") as download_file:
        file_content = requests.get(code_url).content
        download_file.write(file_content)


def _extract_files():
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall("./temp")


def _replace_feature_files(output=True):
    old_files = os.listdir(("./features"))

    for file in old_files:
        if output:
            print(f"\n\033[92m[INFO]:\033[00m Deleting old feature file: {file}\n")
        os.remove(f"./features/{file}")

    new_files = os.listdir("./temp/J-I-B-main/features")

    for file in new_files:
        file_path = "./temp/J-I-B-main/features/" + file
        if output:
            print(f"\n\033[92m[INFO]:\033[00m Copying feature from update: {file}")
        copyfile(file_path, f"./features/{file}")


def _delete_unused_files(output=True):
    if output:
        print(f"\n\033[92m[INFO]:\033[00m Deleting unused files...")
    try:
        rmtree("./temp")
    except Exception as e:
        print('\n\033[91m[ERROR]:\033[00m Error by deleting ./temp folder. Error Message: %s' % e)
        exit()


def update(output=True):
    if _check_update():
        _download()
        _extract_files()
        _replace_feature_files(output=output)
        _delete_unused_files(output=output)
        print("\n\033[92m[INFO]:\033[00m Update successfully.")


if __name__ == '__main__':
    update()
