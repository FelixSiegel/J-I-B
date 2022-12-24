from os import listdir
import re


def pack(dir="features", auto=False):
    files = listdir(dir)
    files.sort(key=lambda test_string: list(map(int, re.findall(r'\d+', test_string)))[0])

    install = []
    if not auto:
        print("\033[93m [WARN]:\033[00m You can turn features on/off, but beware, disabling the wrong functions can "
              "crash the bot.")
        for file in files:
            userinput = input(f'\n\nDo you want install following feature (y (yes) or n (no)): {file} \n')
            while True:
                if userinput == "y":
                    install.append(file)
                    break
                if userinput == "n":
                    break
                else:
                    userinput = input(f"\nIncorrect Answer! Use 'y' for yes or 'n' for no: ")
    else:
        install = files
    new_code_string = ""
    for installing in install:
        path = f"{dir}/{installing}"
        new_code_string = new_code_string + "\n" + open(path, "r").read()
    return new_code_string


if __name__ == '__main__':
    with open("output.py", "w") as output:
        code = pack()
        output.write(code)
    print("\n\033[92m[INFO]:\033[00m Your selected feature are included successfully!\n")