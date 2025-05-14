import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from yandexgptlite import YandexGPTLite

form_router = Router()
dp = Dispatcher()
BOT_TOKEN = "7891329286:AAGHiWkeaR0xZkwUdkIytk1feOnrodJscjk"
account = YandexGPTLite('b1gvp4l65bsipa1tnks5', 'y0__xCXvfP0AxjB3RMgm-2BjRNWOhJNqnlFJ0vKqYH-yiYZdKtvqw')
logger = logging.getLogger(__name__)


class Form(StatesGroup):
    tags = State()
    hard_lvl = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.set_state(Form.tags)
    await message.answer(
        "Привет, я бот, который поможет вам выбрать задачу для решения!\n"
        "Напишите, задачи каких типов вас интересуют."
        "Вы можете остановить работу, послав команду /stop.",
    )


@form_router.message(Command("stop"))
@form_router.message(F.text.casefold() == "stop")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Остановились на шаге %r", current_state)
    await state.clear()
    await message.answer(
        "Всего доброго!",
    )


@form_router.message(Form.tags)
async def process_locality(message: Message, state: FSMContext):
    req = message.text
    print(req)
    text = account.create_completion(
        f'Приведи теги задач с сайта Codeforces.com которые подойдут данному запросу."{req}". В качестве ответа отправь только теги.',
        '0', system_prompt='Выписывай теги через запятую')
    tags = text.split(', ')
    print(tags)
    await message.answer(f"Тогда тебе следует решать задачи с тегами {text}")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    asyncio.run(main())
