from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from settings import TG_TOKEN


# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=TG_TOKEN)
dp: Dispatcher = Dispatcher(bot)


# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: types.Message):
    await message.answer('Привет!\nЭто тестовый бот для обучения')


# Этот хэндлер будет срабатывать на команду "/help"
async def process_help_command(message: types.Message):
    await message.answer(
        'Это тестовый бот для обучения.\n'
        'Сейчас он должен научиться играть в игру "Угадай число"\n'
        'Для начала игры введите "Да", "Давай" или "Сыграем"')


# Этот хэндлер должен срабатывать на "Да", "Давай" или "Сыграем"
async def process_yes_command(message: types.Message):
    await message.answer('Это число')


# Этот хэндлер должен срабатывать на "/stat"
async def process_stat_command(message: types.Message):
    await message.answer('Это число')


    # Этот хэндлер должен срабатывать на "/cancel"
async def process_cancel_command(message: types.Message):
    await message.answer('Это число')


# Этот хэндлер должен срабатывать на число
async def process_number_command(message: types.Message):
    await message.answer('Это число')


# Этот хэндлер будет срабатывать на любые другие текстовые сообщения
async def send_echo(message: types.Message):
    await message.reply(message.text)


# Регистрируем хэндлеры
dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(process_help_command, commands='stat')
dp.register_message_handler(process_help_command, commands='cancel')
dp.register_message_handler(process_number_command,
                            Text([str(x) for x in range(100)]))
dp.register_message_handler(send_echo)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
