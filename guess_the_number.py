from environs import Env
from random import randint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text


env = Env()              # Создаем экземпляр класса Env
env.read_env()           # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

tg_token = env('TG_TOKEN')     # Сохраняем значение переменной окружения в переменную bot_token
admin_id = env.int('ADMIN_ID')   # Преобразуем значение переменной окружения к типу int
                                 # и сохраняем в переменной admin_id


# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=tg_token)
dp: Dispatcher = Dispatcher(bot)

# Словарь в котором храниться статистика игры
game = dict(hidden_number=0,
            count=0,
            game_started=False,
            stat_game_total=0,
            stat_game_canceled=0,
            stat_game_won=0)


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
    if game['game_started']:
        ANSWER = 'Игра уже запущена'
    else:
        game['game_started'] = True
        game['stat_game_total'] += 1
        game['hidden_number'] = randint(0, 99)
        game['count'] = 5
        ANSWER = ("Я загадал число от 0 до 99, попробуй отгадать,"
                  f" у тебя {game['count']} попыток")
    await message.answer(ANSWER)


# Этот хэндлер должен срабатывать на "/stat"
async def process_stat_command(message: types.Message):
    ANSWER = (f"Всего игр начато {game['stat_game_total']}\n"
              f"выиграно игр {game['stat_game_won']}\n"
              f"отменено игр {game['stat_game_canceled']}")
    await message.answer(ANSWER)


# Этот хэндлер должен срабатывать на "/cancel"
async def process_cancel_command(message: types.Message):
    if game['game_started']:
        game['game_started'] = False
        game['stat_game_canceled'] += 1
        ANSWER = ('Игра отменена\n'
                  'для новой игры введите "Да", "Давай" или "Сыграем"')
    else:
        ANSWER = 'Игра не запущена'
    await message.answer(ANSWER)


# Этот хэндлер должен срабатывать на число
async def process_number_command(message: types.Message):
    if game['game_started']:
        game['count'] -= 1
        number = int(message['text'])
        diff = game['hidden_number'] - number

        if diff == 0:
            game['game_started'] = False
            game['stat_game_won'] += 1
            ANSWER = (f"Ты угадал c {5-game['count']} попытки -"
                      f" загаданное число {game['hidden_number']}")
        elif game['count'] == 0:
            game['game_started'] = False
            ANSWER = ("У тебя не осталось попыток -"
                      f" загаданное число {game['hidden_number']}")
        elif diff < 0:
            ANSWER = (f"Загаданное число меньше {number},"
                      f" у тебя осталось {game['count']} попытки")
        elif diff > 0:
            ANSWER = (f"Загаданное число больше {number},"
                      f" у тебя осталось {game['count']} попытки")
    else:
        ANSWER = 'Для начала игры введите "Да", "Давай" или "Сыграем"'
    await message.answer(ANSWER)


# Этот хэндлер будет срабатывать на любые другие текстовые сообщения
async def send_echo(message: types.Message):
    if game['game_started']:
        ANSWER = ('Загадано число от 0 до 99,'
                  f" осталось {game['count']} попытки")
    else:
        ANSWER = ('Сейчас бот умее только играть в "Угадай число"\n'
                  'Для начала игры введите "Да", "Давай" или "Сыграем"')
    await message.answer(ANSWER)


# Регистрируем хэндлеры
dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(process_stat_command, commands='stat')
dp.register_message_handler(process_cancel_command,
                            Text(equals=['Хватит', "Надоело", "Стоп"],
                                 ignore_case=True))
dp.register_message_handler(process_number_command,
                            Text([str(x) for x in range(100)]))
dp.register_message_handler(process_yes_command,
                            Text(equals=["Да", "Давай", "Сыграем", "Yes"],
                                 ignore_case=True))
dp.register_message_handler(send_echo)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
