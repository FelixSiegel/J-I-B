# RULE System

# -----------------------------------------------------
# DEFINE_SERVER_RULES command
# define rules for your server -> if call function modal will pop up
@bot.command(
    name="define_server_rules",
    description="You can define your own rule for your Server.",
    default_member_permissions=interactions.Permissions.ADMINISTRATOR
)
async def define_server_rules(ctx: interactions.CommandContext):
    modal = interactions.Modal(
        title="Define a new Rule",
        custom_id="rule_modal",
        components=[
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                custom_id="title",
                label="Choose a title for your Rules"
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.PARAGRAPH,
                custom_id="content",
                label="Write your rule content here."
            )
        ]
    )
    await ctx.popup(modal)
    await ctx.send("Modal was send!", ephemeral=True)

# -----------------------------------------------------
# MODAL component
# manage the modal for entering server rules data to your server
@bot.modal("rule_modal")
async def set_server_rule(ctx: interactions.CommandContext, title: str, content: str):
    # write data first to json-file
    servers[ctx.guild.name]["server_rules"].update({"title": title, "content": content})
    with open("./data/server_datas.json", "w") as sI:
        json.dump(servers, sI, indent=4)

    # create select-menu for answer -> choose a role, user gets after accepting
    select_menu = interactions.SelectMenu(
        options=[],
        placeholder="Choose role",
        custom_id="rule_role_choose",
        max_values=1
    )
    options = []
    for role in ctx.guild.roles:
        options.append(
            interactions.SelectOption(
                label=str(role.name),
                value=int(role.id),
            )
        )
    select_menu.options = options

    await ctx.send("Please choose a role, that people get, when they agree to your rules.", components=select_menu,
                   ephemeral=True)

# -----------------------------------------------------
# RULE_ACCEPT_CHOOSER component
# send the new rules with a button for accepting and getting specified role
@bot.component("rule_role_choose")
async def rules_accept_role(ctx: interactions.ComponentContext, choosen_roles: str):
    print(f"Selected role is: {choosen_roles[0]}")
    servers[ctx.guild.name]["server_rules"].update({"rules_accept_role": choosen_roles[0]})
    with open("./data/server_datas.json", "w") as sI:
        json.dump(servers, sI, indent=4)

    embed = interactions.Embed()
    embed.title = servers[ctx.guild.name]["server_rules"]["title"]
    embed.description = servers[ctx.guild.name]["server_rules"]["content"]
    embed.color = int(('#%02x%02x%02x' % (90, 232, 240)).replace("#", "0x"), base=16)

    button = interactions.Button(style=interactions.ButtonStyle.SUCCESS, label="Accept",
                                 custom_id="add_rule_accept_role")
    await ctx.channel.send(embeds=embed, components=button)
    await ctx.send("Rules were successfully set up!", ephemeral=True)

# -----------------------------------------------------
# RULE-BUTTON component
# Component for the Accept-Button -> called if clicked -> give role to user
@bot.component("add_rule_accept_role")
async def func(ctx: interactions.ComponentContext):
    rule_accept_role_id = servers[ctx.guild.name]["server_rules"]["rules_accept_role"]
    # check if user has role or not
    if (ctx.author.roles is None) or (not (interactions.Snowflake(rule_accept_role_id) in ctx.author.roles)):
        # if not add role to user
        await ctx.author.add_role(rule_accept_role_id, int(ctx.guild_id))
        await ctx.send("You can now use the Server", ephemeral=True)
    else:
        # if already has, send only a message to the user
        await ctx.send("You already have the role for accepting to the rules!", ephemeral=True)

# -----------------------------------------------------
# RULES command
# send the actually rules
@bot.command(
    name="rules",
    description="Shows the rules of the server",
)
async def rules(ctx: interactions.CommandContext):
    if servers[ctx.guild.name]["server_rules"] == {}:
        return await ctx.send("No Rules specified! Please add rules via `/rule_add` or a description via "
                              "`/add_rule_description`– For more infos type `/help`")
    embed = interactions.Embed()
    embed.title = servers[ctx.guild.name]["server_rules"]["title"]
    embed.description = servers[ctx.guild.name]["server_rules"]["content"]
    embed.color = int(('#%02x%02x%02x' % (90, 232, 240)).replace("#", "0x"), base=16)
    await ctx.send(embeds=embed)

# ======================================================================================================================