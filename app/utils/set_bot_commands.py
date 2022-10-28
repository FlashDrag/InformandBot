from aiogram import Bot
from aiogram.types.bot_command import BotCommand
import json

'''
key - команда; value - description
Словарь кастомных комманд админа,
которые загружаются в главное меню в группе,
и используються для получения определенного контента с БД,
записанного админом через админку в боте.
Полная информация сохранена в БД: command, description, content
В словарь периодически загружаются комманды и описания
для ускорения работы фильтра `CommandFilter()` from app.filters.user,
который проверяет апдейты на соответствующие комманды
'''

my_commands: dict = {}


# TODO Установить по умолчанию комманды которые будут отображаться только в приватном скоупе
async def set_default_commands(dp):
    commands = [
        # BotCommand(command="/start", description="START ✅"),
        # BotCommand(command="/info", description="INFO⚠️"),
        BotCommand(command="/cancel", description="CANCEL ❌")
    ]
    await dp.bot.set_my_commands(commands)


async def update_my_commands(command, description, bot: Bot):
    my_commands[command] = description
    commands = [BotCommand(command=com, description=descr)
                for com, descr in my_commands.items()]
    await bot.set_my_commands(commands)


# TODO Комманды переодично подгружаються с БД в my_commands
# а с my_commands устаннавливаються
async def periodic_commands_update(dp):
    with open('app/utils/db.json', encoding='utf8') as db:
        data = json.load(db)

    my_commands = {key: value['description']
                   for d in data for key, value in d.items()}

    commands = [BotCommand(command=com, description=descr)
                for com, descr in my_commands.items()]
    await dp.bot.set_my_commands(commands)
    print(f'My coomands: {await dp.bot.get_my_commands()}')
    print(f'My dict: {my_commands}')
