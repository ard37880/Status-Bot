from nextcord.ext import application_checks
from nextcord import Interaction, SlashOption, Intents, Embed, Status
import nextcord
from apikeys import discord_bot_token

bot_ids = [1200274769354969148, 1201291463628169317, 1200979708175712358, 1214994240476815471, 1215055130152411136, 1216565327513518164, 1217641990993481738, 1215510959108657165]
channel_id = 1206104996911775794  

intents = Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True
client = nextcord.Client(intents=intents)

last_known_statuses = {bot_id: None for bot_id in bot_ids}


global status_message_ids  
status_message_ids = {}

async def post_status_update(channel):
    global status_message_ids  
    if channel.id not in status_message_ids:
        status_message_ids[channel.id] = []

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
        sent_message = await channel.send(embed=embed)  
        status_message_ids[channel.id].append(sent_message.id)


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

@client.slash_command(name="clear_status", description="Remove all messages sent by '/status'")
async def clear_status(interaction: Interaction):
    if interaction.channel.id in status_message_ids:
        message_ids = status_message_ids[interaction.channel.id]
        for message_id in message_ids:
            try:
                msg = await interaction.channel.fetch_message(message_id)
                await msg.delete()
            except Exception as e:
                print(f"Failed to delete message {message_id}: {e}")
        status_message_ids[interaction.channel.id] = []
        await interaction.response.send_message("Status messages cleared.", ephemeral=True)
    else:
        await interaction.response.send_message("No status messages to clear.", ephemeral=True)

client.run(discord_bot_token)
