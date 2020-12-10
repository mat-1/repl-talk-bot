import server, discordbot

server.start_server(
	discordbot.discord_client.loop,
	discordbot.start_bot(),
	discordbot.discord_client
)
