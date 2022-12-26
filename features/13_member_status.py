# ======================================================================================================================
# MEMBER-STATUS Functionality
@bot.event
async def on_guild_member_add(ctx: interactions.GuildMember):
    # If new user joined Guild -> update Total-member dump
    total_member_channel = await interactions.get(bot, interactions.Channel, object_id=932174956937228298)
    guild = await interactions.get(bot, interactions.Guild, object_id=int(ctx.guild_id))
    await total_member_channel.set_name(f'Total Members: {guild.member_count}')
    sys_channel = await interactions.get(bot, interactions.Channel, object_id=int(guild.system_channel_id))
    embed = interactions.Embed()
    embed.title = f"Welcome to Ice Topia :wave:"
    embed.description = f"Welcome {ctx.mention}! Thank you for join this Server! I hope you have fun here and find \
    some friends :v:"
    embed.color = int(('#%02x%02x%02x' % (90, 232, 240)).replace("#", "0x"), base=16)
    await sys_channel.send(embeds=embed)


@bot.event
async def on_guild_member_remove(ctx):
    # If user left the Guild -> update Total-member dump
    total_member_channel = await interactions.get(bot, interactions.Channel, object_id=932174956937228298)
    memberCount = int(total_member_channel.name.split(": ")[1])  # because ctx is none
    await total_member_channel.set_name(f'Total Members: {memberCount}')

