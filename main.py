from pack_feature import pack

print("Building Bot.....................")
bot_code = pack(auto=True)
print("Starting Bot ..............")
#clear screen
print("\n" * 999999)
exec(bot_code)