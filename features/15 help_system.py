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
