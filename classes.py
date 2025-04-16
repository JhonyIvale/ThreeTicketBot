import discord
from discord.utils import get


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # No timeout = persistent view
    # creating the button
    @discord.ui.button(label="Open", style=discord.ButtonStyle.green, custom_id="persistent_open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if discord.utils.get(interaction.guild.channels,name=f'ticket-{interaction.user.name}') == None:
            # creates the ticket channel
            ticket_manager = get(interaction.guild.roles, name="Ticket-Manager")
            # permission to the channel
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),  # Hide from everyone
                ticket_manager: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
            }
            await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}',overwrites=overwrites)
            # gets the ticket channel
            channel = discord.utils.get(interaction.guild.channels, name=f'ticket-{interaction.user.name}')
            # send a message in the channel
            await channel.send(view=TicketCloseView())
            # send a message in the channel
            await interaction.response.send_message("Ticket Opened!", ephemeral=True)
        else:
            await interaction.response.send_message("Ticket already exists!", ephemeral=True)
# create the class of the button
class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # No timeout = persistent view
    # creating the button
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="persistent_close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
       await interaction.channel.delete()