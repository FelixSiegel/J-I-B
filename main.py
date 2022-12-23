import interactions
import json
from sys import exit
import praw
# using later Async Praw
from random import randint

# reddit api stuff:
client_id = ""
client_secret = ""
user_agent = ""

# try to load necessary variables of bot -> if Error close script
try:
    with open("./data/server_datas.json", "r") as sI:
        servers: dict = json.load(sI)

except Exception as e:
    print(f"\n\033[91m[ERROR]:\033[00m Error occurred on loading JSON-File with the server datas.\nError-Code: {e}\n")
    # if cant loaded
    exit()

# set Variables
guild_ids = [servers[server]["id"] for server in servers]  # server ids
muted_users = []  # list of user who muted

# define Bot client variable
bot = interactions.Client(token=input("Please enter your Bot-Token: "),
                          intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS,
                          presence=interactions.ClientPresence(
                              activities=[interactions.PresenceActivity(
                                  name="/help",
                                  type=interactions.PresenceActivityType.WATCHING)],
                              status=interactions.StatusType.ONLINE
                          )
                          )


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
# MUTE command
@bot.command(
    name="mute",
    description="Command to mute a user",
    default_member_permissions=interactions.Permissions.MUTE_MEMBERS,
    options=[
        interactions.Option(
            name="user",
            description="User you want to mute",
            type=interactions.OptionType.USER,
            required=True,
        ),
    ],
)
async def mute(ctx: interactions.CommandContext, user: interactions.User):
    await ctx.send(f"{user.mention} has been muted!")
    muted_users.append(user.username)


# ======================================================================================================================
# MESSAGE-DELETE command
@bot.command(
    name="msg_delete",
    description="Deletes all last count messages",
    default_member_permissions=interactions.Permissions.MANAGE_MESSAGES,
    options=[
        interactions.Option(
            name="count",
            description="Count of messages that should deleted",
            type=interactions.OptionType.INTEGER,
            required=False
        ),
    ],
)
async def msg_delete(ctx: interactions.CommandContext, count: int = 1):
    # check if count is a correct value
    if not isinstance(count, int) or count <= 0:
        return await ctx.send("False input! Value needs to be a number higher the 0", ephemeral=True)

    # get channel and then delete messages using purge-function
    channel = await interactions.get(bot, interactions.Channel, object_id=int(ctx.channel_id))
    await channel.purge(count)  # delete messages
    await ctx.send(f"Deleted last {count} messages in this channel!", ephemeral=True)


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


# =====================================================================================================================
# MEME generator command
@bot.command(
    name="meme",
    description="Post a random meme",
)
async def meme(ctx: interactions.CommandContext):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    meme_submission = reddit.subreddit('memes').hot()
    post_to_pick = randint(0, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in meme_submission if not x.stickied)

    await ctx.send(f"**{submission.title}**\n{submission.url}")


# =====================================================================================================================
# HELP command
@bot.command(
    name="help",
    description="Sends help menu to all commands and functions",
)
async def help_menu(ctx: interactions.CommandContext):
    # Create Embed Message
    embed = interactions.Embed()
    embed.title = "Help menu of J-I-B Bot – Page 1"
    with open("data/help_doc.json", "r") as fo:
        help_pages: dict = json.load(fo)
    embed.description = help_pages["page1"]["description"]
    for field in help_pages["page1"]["fields"].keys():
        embed.add_field(field, help_pages["page1"]["fields"][field])
    embed.color = int(('#%02x%02x%02x' % (124, 255, 48)).replace("#", "0x"), base=16)

    # Create Next and Last Page button row
    back_btn = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="« Back",
        custom_id="back_button",
    )

    next_btn = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="Next »",
        custom_id="next_button",
    )

    wiki_btn = interactions.Button(
        style=interactions.ButtonStyle.LINK,
        label="Wiki",
        url="https://github.com/FelixSiegel/J-I-B/wiki",
    )

    row = interactions.ActionRow.new(back_btn, next_btn, wiki_btn)
    await ctx.send(embeds=embed, components=row)


@bot.component("back_button")
async def func(ctx: interactions.ComponentContext):
    # get current page
    cur_page = int(ctx.message.embeds.pop().title.split(" ")[-1])
    # if already at page 1 -> return
    if cur_page == 1:
        await ctx.send("You already at page 1!", ephemeral=True)
        return
    # else load new content into embed
    embed = interactions.Embed()
    embed.title = f"Help menu of J-I-B Bot – Page {cur_page - 1}"
    with open("data/help_doc.json", "r") as fo:
        help_pages: dict = json.load(fo)
    if "description" in help_pages[f"page{cur_page - 1}"].keys():
        embed.description = help_pages[f"page{cur_page - 1}"]["description"]
    if help_pages[f"page{cur_page - 1}"]["fields"].keys():
        for field in help_pages[f"page{cur_page - 1}"]["fields"].keys():
            embed.add_field(field, help_pages[f"page{cur_page - 1}"]["fields"][field])
    embed.color = int(('#%02x%02x%02x' % (124, 255, 48)).replace("#", "0x"), base=16)
    # edit message
    await ctx.edit(embeds=embed)


@bot.component("next_button")
async def func(ctx: interactions.ComponentContext):
    # get current page
    cur_page = int(ctx.message.embeds.pop().title.split(" ")[-1])
    # if already at last page -> return
    with open("data/help_doc.json", "r") as fo:
        help_pages: dict = json.load(fo)
    if len(help_pages) == cur_page:
        await ctx.send("You already at last page!", ephemeral=True)
        return
    # else load new content into embed
    embed = interactions.Embed()
    embed.title = f"Help menu of J-I-B Bot – Page {cur_page + 1}"
    if "description" in help_pages[f"page{cur_page + 1}"].keys():
        embed.description = help_pages[f"page{cur_page + 1}"]["description"]
    for field in help_pages[f"page{cur_page + 1}"]["fields"].keys():
        embed.add_field(field, help_pages[f"page{cur_page + 1}"]["fields"][field])
    embed.color = int(('#%02x%02x%02x' % (124, 255, 48)).replace("#", "0x"), base=16)
    # edit message
    await ctx.edit(embeds=embed)
    # await ctx.send(embeds=embed)


bot.start()
