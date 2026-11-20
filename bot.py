import asyncio
import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from services.categories import get_categories
from services.random_word import get_random_word
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.keyboards import main_keyboard, start_keyboard, categories_keyboards, word_keyboard
from services.create_game import get_telegram_id, set_telegram_id, get_word_gameid, get_game_id, change_status_gameid, get_status_gameid
from services.init_db import generate_categories, generate_words
from services.init_words import init_words

from os import getenv


from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

storage = MemoryStorage()
dp = Dispatcher()
router = Router()

dp.include_router(router)

current_categories_id = []

class Form(StatesGroup):
    waiting_for_difficult = State()
    waiting_for_categories = State()
    playing_game = State()

CATEGORIES_NAME = {
    "easy" : "Легкая сложность",
    "medium" : "Средняя сложность",
    "hard" : "Сложная сложность"
}


@dp.message(CommandStart())
async def start(message: Message, state:FSMContext) -> None:
    await message.answer("Привет! Добро пожаловать в Крокодила!",reply_markup=main_keyboard())
    await state.set_state(Form.waiting_for_difficult)

@dp.message(Command("word"))
async def check(message: Message, command: CommandObject):
    if command.args is None:
        print("STOP 1: нет аргументов")
        return await message.answer("Напиши слово!")

    id_game = get_game_id(message.chat.id)
    if id_game is None:
        print("STOP 2: игра не найдена")
        return

    word = get_word_gameid(id_game)
    telegram_id_creator = get_telegram_id(message.from_user.id, id_game)

    if telegram_id_creator == message.from_user.id or telegram_id_creator is None:
        print("STOP 3: проблема с ID показывающего")
        return

    if get_status_gameid(id_game) != "playing":
        print("STOP 4: игра не playing")
        return
    
    if command.args.lower() == word.lower():
        await message.answer("Всё правильно!")
        change_status_gameid(id_game, "ended")

    else:
        await message.answer("Нет, попробуй другое слово!")

@dp.message(Command("newgame"))
async def new_game(message : Message):
    id_game = get_game_id(message.chat.id)

    result = False

    if id_game is None:
        result = True

    if (get_status_gameid(id_game) in ["ended", "cancelled"]) and not result:
        result = True

    if result:
        await message.answer("Привет! Добро пожаловать в Крокодила!",reply_markup=start_keyboard())
    else:
        await message.answer("У вас есть активные игры! Закончите прошлую")

@router.callback_query(F.data == "start_game")
async def start_game(callback : CallbackQuery) -> None:
    await callback.message.edit_text("Отлично, начинаем, но нужно выбрать сложность",reply_markup=start_keyboard()) 
    await callback.answer()


@router.callback_query(F.data.in_(["easy", "medium", "hard"]))
async def difficulty_selected(callback : CallbackQuery, state: FSMContext) -> None:
    await state.update_data(difficult=callback.data)

    await state.set_state(Form.waiting_for_categories)
    await state.update_data(categories=[])
    data = await state.get_data()

    await callback.message.edit_text(f"Выбрана сложность: {CATEGORIES_NAME[data["difficult"]]}", reply_markup=categories_keyboards([]))
    await callback.answer()

@router.callback_query(F.data.startswith("category:"))
async def category_selected(callback : CallbackQuery, state: FSMContext):
    id = callback.data.split(":")[1]
    data = await state.get_data()
    categories = data.get("categories", [])

    if id in categories:
        categories.pop(categories.index(id))
    else:
        categories.append(id)
    await state.update_data(categories=categories)

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=categories_keyboards(categories))

@router.callback_query(F.data == "confirm")
async def confirm_categories(callback : CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Form.playing_game)
    data = await state.get_data()
    
    dif = data["difficult"]
    cat = data["categories"]
    
    get_random_word(callback.message.chat.id, cat, dif)
    await callback.message.edit_text(f"Отлично, я загадал слово!\n\t\t\t\t\t\t\t\t\t\tКто первый?", reply_markup=word_keyboard())

@router.callback_query(F.data == "get_word")
async def get_word_telegramid(callback : CallbackQuery, state: FSMContext):
    id_game = get_game_id(callback.message.chat.id)

    if id_game is None:
        return await callback.answer("Игра отсутствует!")

    if get_status_gameid(id_game) in ["ended", "canceled"]:
        return await callback.answer("Игра закончена!")

    if get_status_gameid(id_game) == "waiting":
        change_status_gameid(id_game, "playing")

    
    telegram_id = get_telegram_id(callback.from_user.id,id_game)

    if telegram_id == callback.from_user.id:
        await callback.answer(f"🤫{get_word_gameid(id_game)}🤫")
    else:
        await callback.answer("Иди угадывай")

    # await callback.answer()

async def main() -> None:
    get_categories()
    init_words()
    generate_categories()
    generate_words()

    bot = Bot(token=getenv("BOT_TOKEN"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())