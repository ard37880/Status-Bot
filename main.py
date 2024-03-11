from nextcord.ext import application_checks
from nextcord import Interaction, SlashOption, Intents, Embed, Status
import nextcord
from apikeys import discord_bot_token

bot_ids = [BOT IDs HERE]
channel_id = YOUR CHANNEL ID HERE  

intents = Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True
client = nextcord.Client(intents=intents)

last_known_statuses = {bot_id: None for bot_id in bot_ids}

async def post_status_update(channel):
    for bot_id in bot_ids:
        bot = await client.fetch_user(bot_id)
        embed_color = 0x00ff00 
        
        status_description = "Status: Unknown"

        if bot.bot:
            for guild in client.guilds:
                member = guild.get_member(bot.id)
                if member:
                    status_description = f"Status: {member.status}"
                    if member.status == Status.offline:
                        embed_color = 0xff0000  
                    break  

        embed = Embed(title=f"Bot Status: {bot.name}", color=embed_color)
        embed.add_field(name="Current Status", value=status_description, inline=False)
        await channel.send(embed=embed)


@client.event
async def on_member_update(before, after):
    if after.id in bot_ids and after.bot and before.status != after.status:
        channel = client.get_channel(channel_id)
        if channel: 
            await post_status_update(channel) 
        last_known_statuses[after.id] = after.status

@client.slash_command(name="status", description="Check the online status of specified bots")
async def status(interaction: Interaction):
    await post_status_update(interaction.channel)


client.run(discord_bot_token)
