import praw
from random import randint

client_id = ""
client_secret = ""
user_agent = ""


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

