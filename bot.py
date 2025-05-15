import asyncio
import logging

import aiogram
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from yandexgptlite import YandexGPTLite

from codeforcerequest import request_find_problem
from tokens import BOT_TOKEN

form_router = aiogram.Router()
dp = aiogram.Dispatcher()
account = YandexGPTLite('b1gvp4l65bsipa1tnks5', 'y0__xCXvfP0AxjB3RMgm-2BjRNWOhJNqnlFJ0vKqYH-yiYZdKtvqw')
cf_tags = ["2-sat", "binary search", "bitmasks", "brute force", "chinese remainder theorem", "combinatorics",
           "constructive algorithms", "data structures", "dfs and similar", "divide and conquer", "dp",
           "dsu", "expression parsing", "fft", "flows", "games", "geometry", "graph matchings", "graphs",
           "greedy", "hashing", "implementation", "interactive",
           "math", "matrices", "meet-in-the-middle", "number theory", "probabilities", "schedules",
           "shortest paths", "sortings", "string suffix structures", "strings", "ternary search", "trees",
           "two pointers"]

logger = logging.getLogger(__name__)


class Form(StatesGroup):
    tags = State()
    hard_lvl = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.set_state(Form.tags)
    await message.answer(
        "Привет, я бот, который поможет вам выбрать задачу для решения!\n"
        "Напишите, задачи каких типов вас интересуют. "
        "Вы можете остановить работу, послав команду /stop.",
    )


@form_router.message(Command("task"))
async def command_task(message: Message, state: FSMContext):
    await state.set_state(Form.tags)
    await message.answer(
        "Напишите, задачи каких типов вас интересуют."
    )


@form_router.message(Command("stop"))
@form_router.message(aiogram.F.text.casefold() == "stop")
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
    await state.set_state(Form.hard_lvl)
    req = message.text
    text = account.create_completion(
        f'"{req}"Просмотри существующие теги задач из этого списка {cf_tags} и подбери подходящие этому запросу.'
        f'В качестве ответа отправь только теги не в кавычках через запятую.',
        '0')
    tags = text.split(', ')
    await state.update_data(tags=tags)
    await message.answer(f"Насколько сложной должна быть задача?")


@form_router.message(Form.hard_lvl)
async def process_hard_lvl(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    req = message.text
    print("fsfs")
    hard_lvl = account.create_completion(
        f'"{req}"По этому запросу выбери сложность от 800 до 3500, где 800 - легкая, а 3500 - невероятно сложная.'
        f'В качестве ответа отправь только число.',
        '0')
    logger.info(f"сложность {hard_lvl}")
    print("fsfs")
    answer = f'''Тогда вам подойдет эти задачи:\n {request_find_problem(';'.join(data['tags']), hard_lvl)}'''
    await message.answer(answer)


async def main():
    bot = aiogram.Bot(token=BOT_TOKEN)
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    asyncio.run(main())
