# ======================================================================================================================
# BAN command
@bot.command(
    name="ban",
    description="Command to ban a user",
    default_member_permissions=interactions.Permissions.BAN_MEMBERS,
    options=[
        interactions.Option(
            name="user",
            description="User you want to ban",
            type=interactions.OptionType.USER,
            required=True,
        ),
        interactions.Option(
            name="reason",
            description="Reason for banning",
            type=interactions.OptionType.STRING,
            required=False,
        ),
    ],
)
async def ban(ctx: interactions.CommandContext, user: interactions.Member, reason: str = None):
    if reason:
        await ctx.guild.ban(user, reason=reason)
        return await ctx.send(f"{user} has been banned because {reason}!")
    else:
        await ctx.guild.ban(user)
        return await ctx.send(f"{user} has been banned")

# ======================================================================================================================
# UNBAN command
@bot.command(
    name="unban",
    description="Command to unban a user",
    default_member_permissions=interactions.Permissions.BAN_MEMBERS,
    options=[
        interactions.Option(
            name="user",
            description="User you want to unban",
            type=interactions.OptionType.USER,
            required=True,
        )
    ],
)
async def unban(ctx: interactions.CommandContext, user):
    await ctx.guild.remove_ban(user)
    await ctx.send(f"has been unbanned!")

# ======================================================================================================================