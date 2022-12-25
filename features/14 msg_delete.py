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

