import asyncio
import os
from webserver import keep_alive

import discord
import disnake
from disnake.ext import commands
from quickstart import addToTable

my_secret = os.environ['KEY']

bot = commands.Bot(command_prefix=commands.when_mentioned,
                   help_command=None,
                   intents=disnake.Intents.all())

#@bot.event
#async def on_command_error(ctx, error):
#  await ctx.send(error)


@bot.event
async def on_ready():
  print(f"Bot {bot.user} is ready to work.")
  await bot.change_presence(status=discord.Status.online,
                            activity=disnake.Game(name="уборку"))


class AddEvent(disnake.ui.Modal):

  def __init__(self):
    components = [
      disnake.ui.TextInput(label="Сикей",
                           placeholder="Введите сюда свой сикей",
                           custom_id="Сикей",
                           max_length=25),
      disnake.ui.TextInput(label="Номер раунда",
                           placeholder="Введите сюда номер раунда",
                           custom_id="Раунд",
                           max_length=10),
      disnake.ui.TextInput(
        label="Сервер",
        placeholder=
        "Сервер писать ТОЛЬКО как в примере (Main, Athara, Echo, Nova, Solaris, Elysium)",
        style=disnake.TextInputStyle.paragraph,
        custom_id="Сервер",
        max_length=7),
      disnake.ui.TextInput(
        label="Тип ивента",
        placeholder=
        "Тип ивента писать ТОЛЬКО как в примере (Мини, Ивент, Крупный, Нек)",
        style=disnake.TextInputStyle.paragraph,
        custom_id="Тип ивента",
        max_length=7),
      disnake.ui.TextInput(
        label="Описание",
        placeholder="Кратко опишите суть ивента, ошибки и недочёты",
        style=disnake.TextInputStyle.paragraph,
        custom_id="Описание",
        max_length=2000),
    ]
    super().__init__(title="Отчёт о ивенте", components=components)

  async def callback(self, inter: disnake.ModalInteraction):
    await inter.response.defer(ephemeral=False)
    embed = disnake.Embed(title="Отчёт о ивенте😎")
    info = list(inter.text_values.values())
    for key, value in inter.text_values.items():
      embed.add_field(name=key.capitalize(), value=value[:1024], inline=False)
    addToTable([info])
    await inter.edit_original_message(embed=embed)


@bot.command(name="ивент")
@commands.has_any_role(921927178529157140, 947424869069488145,
                       942732730729381958, 947424375525744671,
                       1060877000480411659, 1140726126189219850,
                       919315787146223617)
async def create_application(inter: disnake.AppCmdInter):
  modal = AddEvent()
  await inter.response.send_modal(modal=modal)


@create_application.error
async def create_application_error(ctx, error):
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send(
      f'{ctx.author.mention}, простите, но мне не разрешают общаться с незнакомцами. Попросите кого-нибудь выдать вам соответствующую роль'
    )


@bot.command(name="таблица")
@commands.has_any_role(921927178529157140, 947424869069488145,
                       942732730729381958, 947424375525744671,
                       1060877000480411659, 1140726126189219850,
                       919315787146223617)
async def url(inter):
  await inter.send(
    "Конечно, вот ссылка на таблицу :flushedCat: -https://docs.google.com/spreadsheets/d/1ecawqy0N8Bpo0Fh_nyONZZxv9MRFTHdKaZVTeFCGdQI/edit?pli=1#gid=0"
  )


@url.error
async def url_error(ctx, error):
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send(
      f'{ctx.author.mention}, простите, но мне не разрешают общаться с незнакомцами. Попросите кого-нибудь выдать вам соответствующую роль'
    )


@bot.command(name="помощь")
@commands.has_any_role(921927178529157140, 947424869069488145,
                       942732730729381958, 947424375525744671,
                       1060877000480411659, 1140726126189219850,
                       919315787146223617)
async def img(inter):
  await inter.send(
    f'Привет, {inter.author.mention}! Я Аляска - бот для помощи вам в написании отчётов по ивентам! Чтобы добавить новый отчёт, пинганите меня со словом ивент - и я выдам вам окно для заполнения! Если вам нужна таблица, в которую я заполняю ваши отчёты - пинганите меня со словом таблица, и я вам дам ссылку! Правда просто? Спасибо моему папе Ewer за это :flushedCat:'
  )
  await inter.send(file=disnake.File('help.gif'))


@img.error
async def img_error(ctx, error):
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send(
      f'{ctx.author.mention}, простите, но мне не разрешают общаться с незнакомцами. Попросите кого-нибудь выдать вам соответствующую роль'
    )


@bot.command(name="автор")
@commands.has_any_role(921927178529157140, 947424869069488145,
                       942732730729381958, 947424375525744671,
                       1060877000480411659, 1140726126189219850,
                       919315787146223617)
async def img_meme(inter):
  await inter.send(
    "Моим отцом является Ewerall :heart: , который сделал меня для гейм-мастерского сообщества проекта Corvax!"
  )
  await inter.send(file=disnake.File('author.gif'))


@img_meme.error
async def img_meme_error(ctx, error):
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send(
      f'{ctx.author.mention}, простите, но мне не разрешают общаться с незнакомцами. Попросите кого-нибудь выдать вам соответствующую роль'
    )


keep_alive()
bot.run(my_secret)
