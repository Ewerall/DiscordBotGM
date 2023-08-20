import asyncio
import os

import discord
import disnake
from disnake.ext import commands
from quickstart import addToTable
from webserver import keep_alive

bot = commands.Bot(command_prefix="!", help_command=None, intents=disnake.Intents.all())
my_secret = os.environ['KEY']

@bot.event
async def on_command_error(ctx, error):
   await ctx.send(error)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work.")
    await bot.change_presence(status = discord.Status.online, activity=disnake.Game(name="уборку"))

class AddEvent(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Сикей",
                placeholder="Введите сюда свой сикей",
                custom_id="Сикей",
                max_length=25
            ),
            disnake.ui.TextInput(
                label="Номер раунда",
                placeholder="Введите сюда номер раунда",
                custom_id="Раунд",
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Сервер",
                placeholder="Сервер писать ТОЛЬКО как в примере (Main, Athara, Echo, Nova, Solaris, Elysium)",
                style=disnake.TextInputStyle.paragraph,
                custom_id="Сервер",
                max_length=7
            ),
            disnake.ui.TextInput(
                label="Тип ивента",
                placeholder="Тип ивента писать ТОЛЬКО как в примере (Мини, Ивент, Крупный, Нек)",
                style=disnake.TextInputStyle.paragraph,
                custom_id="Тип ивента",
                max_length=7
            ),
            disnake.ui.TextInput(
                label="Описание",
                placeholder="Кратко опишите суть ивента, ошибки и недочёты",
                style=disnake.TextInputStyle.paragraph,
                custom_id="Описание",
                max_length=100
            ),
        ]
        super().__init__(title="Отчёт о ивенте", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        await inter.response.defer(ephemeral = True)
        embed = disnake.Embed(title="Отчёт о ивенте😎")
        info = list(inter.text_values.values())
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False
            )
        addToTable([info])
        await inter.followup.send(embed = embed)


@bot.slash_command(name="eventadd", description="Создать новый отчёт о ивенте")
@commands.has_any_role(921927178529157140, 947424869069488145, 942732730729381958, 947424375525744671, 1060877000480411659, 1140726126189219850, 919315787146223617)
async def create_application(inter: disnake.AppCmdInter):
    modal = AddEvent()
    await inter.response.send_modal(modal=modal)

@create_application.error
async def create_application_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send(f'{ctx.author.mention}, у вас нет подходящей роли, чтобы пользоваться этой командой.')

@bot.slash_command(name="url", description="Дает ссылку на таблицу")
@commands.has_any_role(921927178529157140, 947424869069488145, 942732730729381958, 947424375525744671, 1060877000480411659, 1140726126189219850, 919315787146223617)
async def url(inter):
    await inter.response.send_message("Ссылка на таблицу - https://docs.google.com/spreadsheets/d/1ecawqy0N8Bpo0Fh_nyONZZxv9MRFTHdKaZVTeFCGdQI/edit?pli=1#gid=0")

@url.error
async def url_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send(f'{ctx.author.mention}, у вас нет подходящей роли, чтобы пользоваться этой командой.')

@bot.slash_command(name="help", description="Помощь")
async def img(inter):
    await inter.response.send_message("no.")
    await inter.send(file=disnake.File('cat.gif'))

@bot.slash_command(name="author", description="Автор бота")
async def img_meme(inter):
    await inter.response.send_message("Автором бота является Ewerall, для ГМ сообщества проекта Корвакс")
    await inter.send(file=disnake.File('guh.gif'))


bot.run(my_secret)

