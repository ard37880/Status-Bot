from nextcord.ext import application_checks
from nextcord import Interaction, SlashOption, Intents, Embed, Status
import nextcord
from apikeys import discord_bot_token

# Initialize the client with presence and member intents
bot_ids = [1200274769354969148, 1201291463628169317, 1200979708175712358, 1214994240476815471, 1215055130152411136, 1215510959108657165]
channel_id = 1206104996911775794  # Define your channel ID here

intents = Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True
client = nextcord.Client(intents=intents)

last_known_statuses = {bot_id: None for bot_id in bot_ids}

async def post_status_update(channel):
    # This function now sends separate embeds for each bot
    for bot_id in bot_ids:
        bot = await client.fetch_user(bot_id)
        embed_color = 0x00ff00  # Default green color indicating online or other non-offline statuses
        
        # Default status description for when a bot's status cannot be found
        status_description = "Status: Unknown"

        if bot.bot:
            for guild in client.guilds:
                member = guild.get_member(bot.id)
                if member:
                    # Simplified status description without mentioning the server
                    status_description = f"Status: {member.status}"
                    if member.status == Status.offline:
                        embed_color = 0xff0000  # Red color indicating offline status
                    break  # Stop searching once we find the bot in any server

        # Create and send an embed for this bot
        embed = Embed(title=f"Bot Status: {bot.name}", color=embed_color)
        embed.add_field(name="Current Status", value=status_description, inline=False)
        await channel.send(embed=embed)


@client.event
async def on_member_update(before, after):
    # Only proceed if the member is a bot we're monitoring and there's a status change
    if after.id in bot_ids and after.bot and before.status != after.status:
        # Find a channel to send this information to
        channel = client.get_channel(channel_id)
        if channel:  # Make sure the channel exists
            await post_status_update(channel)  # Pass the channel to the update function
        # Update the last known status regardless of the change
        last_known_statuses[after.id] = after.status

@client.slash_command(name="status", description="Check the online status of specified bots")
async def status(interaction: Interaction):
    await post_status_update(interaction.channel)

# Additional code for the check_bot_status slash command remains the same

# Run the client
client.run(discord_bot_token)
