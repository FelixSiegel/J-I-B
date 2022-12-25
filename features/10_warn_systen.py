# ======================================================================================================================
# WARN command
@bot.command(
    name="warn",
    description="Command to warn a user",
    default_member_permissions=interactions.Permissions.KICK_MEMBERS,
    options=[
        interactions.Option(
            name="user",
            description="User you want to warn",
            type=interactions.OptionType.USER,
            required=True,
        ),
        interactions.Option(
            name="reason",
            description="Reason for warning",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def warn(ctx: interactions.CommandContext, user: interactions.Member, reason: str):
    if user.name == bot.me.name: return await ctx.send("Action not allowed", ephemeral=True)
    if user.name == "Ice Warrior":
        if ctx.author.name in servers[ctx.guild.name]["warns"].keys():
            servers[ctx.guild.name]["warns"][ctx.author.name] += 1
        else:
            servers[ctx.guild.name]["warns"].setdefault(ctx.author.name, 1)
        return await ctx.send(f"Du Kek! Das gibt ne Verwarnung! {ctx.author.mention} was warned for warning Ice! "
                              f"({user.mention} has {servers[ctx.guild.name]['warns'][ctx.author.name]} warns)")

    # check if the user has already been warned
    if user.name in servers[ctx.guild.name]["warns"].keys():
        servers[ctx.guild.name]["warns"][user.name] += 1
    else:
        servers[ctx.guild.name]["warns"].setdefault(user.name, 1)
    # update json file
    with open("./data/server_datas.json", "w") as sI:
        json.dump(servers, sI, indent=4)
    # send message
    await ctx.send(f"{user.mention} has been warned for {reason}! ({user.mention}\
    has {servers[ctx.guild.name]['warns'][user.name]} warns)")

# ======================================================================================================================