# ======================================================================================================================
# ON-READY event
@bot.event
async def on_ready():
    print("\n\033[92m[INFO]:\033[00m Bot successfully started!\n")

    # Total and Online Member counters -> only for own test-server
    try:
        guild = await interactions.get(bot, interactions.Guild, object_id=931944391768170516)
        total_member_channel = await interactions.get(bot, interactions.Channel, object_id=932174956937228298)

        await total_member_channel.set_name(f'Total Members: {guild.member_count}')
    except Exception as e:
        print(f"\n\033[91m[ERROR]:\033[00m Error occurred on setting name for Members-Channel"
              f"\nError-Code: {e}\n")

# ======================================================================================================================