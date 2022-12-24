from os import listdir
import re
def pack(dir="features",auto=False):
    files = listdir(dir)
    files.sort(key=lambda test_string: list(
    map(int, re.findall(r'\d+', test_string)))[0])

    install = []
    if auto == False:
        print("You can enable or disable features if you disable the wrong ones the Bot could BROKEN")
        for file in files:
            while True:
                userinput = input(f'{file}\n to you want install this feature? yes(y) no(standard=n)')
                if not userinput == "y" or userinput == "n":
                    continue
                else:
                    if userinput == "y":
                        install.append(file)
                    else:
                        pass
                    break
    else:
        install = files
    new_code_string = ""
    for installing in install:
        path = f"{dir}/{installing}"
        new_code_string = new_code_string + "\n" + open(path,"r").read()
    return new_code_string

if __name__ == '__main__':
    with open("output.py","w") as output:
        code = pack()
        output.write(code)
    print("Saved your botpy to output.py")