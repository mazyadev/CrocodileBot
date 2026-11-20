from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.categories import categories_dict

def start_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="Легкая сложность", callback_data="easy")
  builder.button(text="Средняя сложность", callback_data="medium")
  builder.button(text="Тяжелая сложность", callback_data="hard")
  builder.adjust(1)  # Выстроит все кнопки в 1 столбец
  return builder.as_markup()


def main_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="Начать игру", callback_data="start_game")
  builder.adjust(1)
  return builder.as_markup()

def word_keyboard():
   builder = InlineKeyboardBuilder()
   builder.button(text='Получить слово', callback_data="get_word")
   builder.adjust(1)
   return builder.as_markup()

def categories_keyboards(selected_categories):
    builder = InlineKeyboardBuilder()
    for i in categories_dict:
        add_string = ""
        if str(i) in selected_categories:
          add_string += "✓"
        builder.button(text=add_string+categories_dict[i], callback_data=f"category:{i}")

    builder.button(text="Подтвердить", callback_data="confirm")

    builder.adjust(3,3,3,2,1)
    return builder.as_markup()


    