# ON_INVITE event
@bot.event
async def on_guild_create(ctx: interactions.Guild):
    if not ctx.id in guild_ids:
        # add new id to guild_ids list
        guild_ids.append(ctx.id)
        # new entry in server_datas.json
        servers.update({ctx.name: {"id": int(ctx.id), "warns": {}, "server_rules": {}}})
        with open("./data/server_datas.json", "w") as sI:
            json.dump(servers, sI, indent=4)
        # Send welcome message
        embed = interactions.Embed()
        embed.title = "Hey there! :wave:"
        embed.description = "Hello, thank you for adding me to your Server! \n\n" \
                            "If you want to use the full functionality of the " \
                            "bot you have to confer several things first. \nFor more " \
                            "details you should read the **linked wiki** of this bot on GitHub." \
                            " Otherwise you can also call `/help` to briefly look up " \
                            "a command and its function! \n\nHave fun with the bot ^^"
        embed.color = int(('#%02x%02x%02x' % (90, 232, 240)).replace("#", "0x"), base=16)
        channel = await interactions.get(bot, interactions.Channel, object_id=int(ctx.system_channel_id))
        await channel.send(embeds=embed, components=interactions.Button(
            style=interactions.ButtonStyle.LINK,
            label="Wiki",
            url="https://github.com/jumpie07/J-I-B/wiki",
        ))

# =====================================================================================================================