from pymongo import MongoClient
from dotenv import load_dotenv
import discord
from discord.ext import commands
import os
import classes
#Api#

# Carrega as variaveis .env
if os.path.isfile(".env"):
    load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#Permissions#

mongodb_client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
collection = mongodb_client['ticketbot']['servers']

bot = commands.Bot(command_prefix='!', intents=intents)





# Comando para criar o embed com botão

@bot.command()
async def ticketinit(ctx):
    if discord.utils.get(ctx.author.roles, name='Ticket-Manager'):
        if collection.find_one({"id": ctx.guild.id}): # Já foi inicializado
            await ctx.send("Its already initialized.")
            return
    

        embed = discord.Embed(
            color=discord.Color.dark_red(),
            title="**Open ticket**",
            description="Click in the button to create a ticket"
        )

        message = await ctx.send(embed=embed, view=classes.TicketView())

        collection.insert_one({
            "id": ctx.guild.id,
            "channel": ctx.channel.id,
            "message": message.id
        })

        role = discord.utils.get(ctx.guild.roles, name="Ticket-Manager")
        if role is None:
            await ctx.guild.create_role(name="Ticket-Manager", permissions=discord.Permissions(send_messages=False), reason="Role required for ticket system")
    else:
        await ctx.send("you don't have permission")


@bot.command()
async def ticketreset(ctx):
    if discord.utils.get(ctx.author.roles, name='Ticket-Manager'):
        dados_server = collection.find_one({"id": ctx.guild.id})
        if dados_server == None:
            await ctx.send("Not initialized.")
        channel_id = dados_server['channel']
        message_id = dados_server['message']
        channel = ctx.guild.get_channel(channel_id) or await bot.fetch_channel(channel_id)
        try:
            message = await channel.fetch_message(message_id)
            await message.delete()
            await ctx.send("Server reset successfull!")
        except discord.NotFound:
            await ctx.send("Error deleting message!")
        except discord.Forbidden:
            await ctx.send("The bot does not have permission to delete the message.")
        except discord.HTTPException as e:
            await ctx.send("Error deleting message!")
        
        collection.delete_one({"id": ctx.guild.id})
    else:
       await ctx.send("you don't have permission")   

@bot.event
async def on_ready():
    bot.add_view(classes.TicketView())
    bot.add_view(classes.TicketCloseView())

# Roda o bot (coloque seu token entre as aspas)
bot.run(os.getenv('TOKEN'))