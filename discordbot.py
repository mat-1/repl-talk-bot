from datetime import datetime
import repltalk
import discord
import asyncio
import os

token = os.getenv('token')

discord_client = discord.Client()
repltalk_client = repltalk.Client()

repl_talk_channel_id = 483420106785947650

def datetime_to_seconds(dt):
	epoch = datetime.utcfromtimestamp(0)
	return (dt - epoch).total_seconds()

def filter_posts_after(posts, after=None):
	return list(filter(lambda post: datetime_to_seconds(post.timestamp) > datetime_to_seconds(after), posts))

async def get_new_posts(after=None):
	posts = await repltalk_client.boards.all.get_posts(sort='new')

	posts = filter_posts_after(posts, after)

	return posts

def embed_from_post(post):
	board_name = post.board.name.title()

	embed_title = post.title
	embed_content = post.content[:2048]
	embed_url = post.url
	embed_timestamp = post.timestamp
	embed_color = discord.Embed.Empty

	# Generates the embed
	embed = discord.Embed(
		title=embed_title,
		description=embed_content,
		url=embed_url,
		timestamp=embed_timestamp,
		color=embed_color
	)
	embed.set_author(
		name=post.author.name,
		url=post.url,
		icon_url=post.author.avatar
	)
	embed.set_footer(text=board_name)
	return embed


async def send_new_posts(channel, after):
	returning_timestamp = datetime.utcnow()
	new_posts = await get_new_posts(after)
	print(new_posts)
	for post in new_posts:
		discord_embed = embed_from_post(post)
		await channel.send(embed=discord_embed)

	return returning_timestamp

@discord_client.event
async def on_ready():
	print('Logged in as')
	print(discord_client.user.name)
	print(discord_client.user.id)
	game = discord.Game(
		name=f'Repl Talk',
		type=discord.ActivityType.watching
	)
	await discord_client.change_presence(activity=game)

	repl_talk_channel = discord_client.get_channel(repl_talk_channel_id)

	after = datetime.utcnow()
	while True:
		after = await send_new_posts(repl_talk_channel, after)
		await asyncio.sleep(10)


async def start_bot():
	print('starting bot pog')
	await discord_client.start(token)
