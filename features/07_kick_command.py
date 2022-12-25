# KICK command
@bot.command(
    name="kick",
    description="Command to kick a user",
    default_member_permissions=interactions.Permissions.KICK_MEMBERS,
    options=[
        interactions.Option(
            name="user",
            description="User you want to kick",
            type=interactions.OptionType.USER,
            required=True,
        ),
    ],
)
async def kick(ctx: interactions.CommandContext, user: interactions.User):
    await ctx.guild.kick(user.id)
    await ctx.send(f"{user.mention} has been kicked!")