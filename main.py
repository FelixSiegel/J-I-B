from pack_feature import pack
from updater import update
if __name__ == '__main__':
    print("\n\033[92m[INFO]:\033[00m Looking for updates...........\n")
    update(output=False)
    print("\n\033[92m[INFO]:\033[00m Building Bot..................\n")
    bot_code = pack(auto=True)
    print("\n\033[92m[INFO]:\033[00m Starting Bot..................\n")
    print("\n" * 4)

    # run code
    exec(bot_code)