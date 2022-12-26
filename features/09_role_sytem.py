# ADD-ROLE command
@bot.command(
    name="add_role",
    description="Command to assign a role to a user",
    default_member_permissions=interactions.Permissions.MANAGE_ROLES,
    options=[
        interactions.Option(
            name="user",
            description="User you want to assign a role to",
            type=interactions.OptionType.USER,
            required=True,
        ),
        interactions.Option(
            name="role",
            description="Role you want to assign",
            type=interactions.OptionType.ROLE,
            required=True,
        ),
    ],
)
async def add_role(ctx: interactions.CommandContext, user: interactions.Member, role: interactions.Role):
    # check if the user already has this role
    if role.id in user.roles:
        await ctx.send(f"{user.mention} already has the role {role.name}!", ephemeral=True)
        return
    # assign the role
    await user.add_role(role, ctx.guild_id)
    await ctx.send(f"{user.mention} has been given the role {role.name}!")

# ======================================================================================================================
# REMOVE-ROLE command
@bot.command(
    name="remove_role",
    description="Command to remove a role from a user",
    default_member_permissions=interactions.Permissions.MANAGE_ROLES,
    options=[
        interactions.Option(
            name="user",
            description="User you want to remove a role from",
            type=interactions.OptionType.USER,
            required=True,
        ),
        interactions.Option(
            name="role",
            description="Role you want to remove",
            type=interactions.OptionType.ROLE,
            required=True,
        ),
    ],
)
async def remove_role(ctx: interactions.CommandContext, user: interactions.Member, role: interactions.Role):
    # check if the user does not have the role
    if not (role.id in user.roles):
        await ctx.send(f"{user.mention} doesn't have the role {role.name}!", ephemeral=True)
        return
    # else remove the role
    await user.remove_role(role, ctx.guild_id)
    await ctx.send(f"{user.mention} has been removed the role {role.name}!")
