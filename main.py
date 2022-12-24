from pack_feature import pack
from updater import update
if __name__ == '__main__':
    print("Updating................")
    update(output=False)
    print("Building Bot.....................")
    bot_code = pack(auto=True)
    print("Starting Bot ..............")
    # clear screen
    print("\n" * 999999)
    exec(bot_code)