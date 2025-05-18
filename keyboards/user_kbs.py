from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


filrer_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вид спорта', callback_data='sport'),
        InlineKeyboardButton(text='кэф', callback_data='k'),
        InlineKeyboardButton(text='Дата', callback_data='date')],
    [InlineKeyboardButton(text='Получить прогноз', callback_data='get_predict')]
])

choose_sport_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Футбол', callback_data='sport_soccer'),
        InlineKeyboardButton(text='Хоккей', callback_data='sport_ice-hockey'),
        InlineKeyboardButton(text='Баскетбол', callback_data='sport_basketball')],
    [InlineKeyboardButton(text='Волейбол', callback_data='sport_volleyball'),
        InlineKeyboardButton(text='Теннис', callback_data='sport_tennis'),
        InlineKeyboardButton(text='CS2', callback_data='sport_csgo'),
        InlineKeyboardButton(text='Dota2', callback_data='sport_dota2')],
    [InlineKeyboardButton(text='Бокс', callback_data='sport_boxing'),
        InlineKeyboardButton(text='ММА', callback_data='sport_mma')],
])

k_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1-2', callback_data='k_1_2'),
        InlineKeyboardButton(text='2-4', callback_data='k_2_4'),
        InlineKeyboardButton(text='4-10', callback_data='k_4_10')],
])