from aiogram import Bot, Dispatcher, executor, types
from settings import TG_TOKEN


# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=TG_TOKEN)
dp: Dispatcher = Dispatcher(bot)


# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: types.Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
async def process_help_command(message: types.Message):
    await message.answer('Напиши мне что-нибудь и в ответ'
                         ' я пришлю тебе твое сообщение')


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
async def send_echo(message: types.Message):
    await message.reply(message.text)


# Регистрируем хэндлеры
dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(send_echo)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
