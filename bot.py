import discord
import chatsss
from discord import app_commands
from discord.ext import commands
import json
import random
import qrcode
import os
import shutil
import requests
import cv2

with open('config.json') as f:
    data = json.load(f)
    TOKEN = data["TOKEN"]
    prefix = data["PREFIX"]


async def send_message(message, user_message, is_private):
    try:
        response = chatsss.get_response(user_message)
        if(response == 1): # if there no message
            await message.channel.send("https://www.youtube.com/watch?v=rV5ynCW-kVw")
        if(response == 2):
            await message.channel.send("https://cdn.discordapp.com/attachments/820247891917537280/1104676885662810112/Untitlepain555d.gif")
        if(response == "read"):
            qrnameread = random.randint(1,99999)
            img_url = message.attachments[0].url
            responseqrdownload = requests.get(img_url, stream=True)
            with open(f"image/qrgen/{qrnameread}.png", 'wb') as out_file:
                shutil.copyfileobj(responseqrdownload.raw, out_file)
            del responseqrdownload
            imgreader = cv2.imread(f"image/qrgen/{qrnameread}.png")
            dectector = cv2.QRCodeDetector()
            val,b,c = dectector.detectAndDecode(imgreader)
            if(bool(val) == True):
                await message.channel.send(val)
                if os.path.exists(f"image/qrgen/{qrnameread}.png"):
                    os.remove(f"image/qrgen/{qrnameread}.png")
                else:
                    print("The file does not exist")
            else:
                await message.channel.send("THIS IS NOT QR CODE BRO WTF")
            
        else:
            pass

    except Exception as e:
        print(e)



def run_discord_bot():
    client = commands.Bot(command_prefix="!" , intents= discord.Intents.all())


    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        try:
            synced = await client.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @client.event #read and send message
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        
        if user_message[0] == '&':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
            
    #try slash command
    @client.tree.command(name="uh_hi")
    async def uh_hi(interaction: discord.Interaction):
        await interaction.response.send_message(f"hey {interaction.user.mention}! This is slash command! and hi", ephemeral=True)


    @client.tree.command(name="qr_gen")
    @app_commands.describe(genqr = "สร้าง QR Code จากข้อความ")
    async def qr_gen(interaction: discord.Interaction, genqr: str):
        #await interaction.response.send_message(f"{interaction.user.mention} Said : `{genqr}`")
        qrname = random.randint(1,99999)
        img = qrcode.make(genqr)
        type(img)
        img.save(f"image/qrgen/{qrname}.png")
        await interaction.response.send_message(file=discord.File(f"image/qrgen/{qrname}.png"))
        if os.path.exists(f"image/qrgen/{qrname}.png"):
            os.remove(f"image/qrgen/{qrname}.png")
        else:
            print("The file does not exist")
        
    


    client.run(TOKEN)