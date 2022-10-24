from aiogram.types.bot_command import BotCommand

'''
key - команда; value - description
Словарь кастомных комманд админа,
которые загружаются в главное меню в группе,
и используються для получения определенного контента с БД,
записанного админом через админку в боте.
Полная информация сохранена в БД: command, description, content
В словарь периодически загружаются комманды и описания,
для ускорения работы фильтра `CommandFilter()` from app.filters.user,
который проверяет апдейты на соответствующие комманды
'''

my_commands: dict = {}


# TODO Установить по умолчанию две комманды: start, cancel которые будут работать,
#  а еще лучше отображаться только в приватном скоупе
async def set_default_commands(dp):
    commands = [
        BotCommand(command="/start", description="START ✅"),
        # BotCommand(command="/info", description="INFO⚠️"),
        BotCommand(command="/cancel", description="CANCEL ❌")
        ]
    await dp.bot.set_my_commands(commands)
