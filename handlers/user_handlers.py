from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from parser import get_predict_data
from keyboards.user_kbs import filter_kb, choose_sport_kb, k_kb, date_kb, get_predict_kb
from database.cruds import create_user_if_not_exists, get_user_predict_filter, edit_user_predict_filter
from ai_generator import get_parsed_predict


user_router = Router()


def replace_filter_title(filters: dict) -> dict:
    current_filters = {}
    
    sport_parse = {
        'soccer': 'Футбол',
        'ice-hockey': 'Хоккей',
        'basketball': 'Баскетбол',
        'volleyball': 'Волейбол',
        'tennis': 'Теннис',
        'csgo': 'CS2',
        'dota2': 'Dota2',
        'boxing': 'Бокс',
        'mma': 'ММА'
    }
    date_parse = {
        '2d': '2 дня',
        '24h': '24 часа',
        '12h': '12 часов',
        '6h': '6 часов',
        '2h': '2 часа'
    }
    
    current_filters['sport'] = sport_parse[filters['sport']] if filters['sport'] != 'Не указано' else 'Не указано'
    current_filters['k'] = filters['k'] if filters['k'] != '1-10' else ['1', '10']
    current_filters['date'] = date_parse[filters['date']] if filters['date'] != 'Не указано' else 'Не указано'
    return current_filters


@user_router.message(CommandStart())
async def start_handler(message: Message):
    await create_user_if_not_exists(message.from_user.id)
    await message.answer('<b>Hello, Im a bet-predict bot!</b>', reply_markup=get_predict_kb)


@user_router.message(Command('predict'))
async def predict_handler(message: Message):
    predict_filter = await get_user_predict_filter(message.from_user.id)
    predict_filter = replace_filter_title(predict_filter)
    await message.answer(f'<b>Можете выбрать фильтр для прогноза\n\nСпорт: {predict_filter["sport"]}\nКоэффициент: {predict_filter["k"][0]}-{predict_filter["k"][1]}\nДата: {predict_filter["date"]}</b>',
                            reply_markup=filter_kb)


@user_router.callback_query(F.data == 'start_predict')
async def predict_handler(callback: CallbackQuery):
    await callback.answer()
    predict_filter = await get_user_predict_filter(callback.message.chat.id)
    predict_filter = replace_filter_title(predict_filter)
    await callback.message.answer(f'<b>Можете выбрать фильтр для прогноза\n\nСпорт: {predict_filter["sport"]}\nКоэффициент: {predict_filter["k"][0]}-{predict_filter["k"][1]}\nДата: {predict_filter["date"]}</b>',
                            reply_markup=filter_kb)


@user_router.callback_query(F.data == 'get_predict')
async def get_predict_handler(callback: CallbackQuery):
    await callback.answer()
    
    waiting_message = await  callback.message.answer('<b><i>Анализирую матчи...</i></b>')
    
    predict_filter = await get_user_predict_filter(callback.from_user.id)
    predict_data = await get_predict_data(predict_filter)
    
    
    if not predict_data:
        await callback.message.answer('<b>Матчи не найдены</b>', reply_markup=filter_kb)
        try: await waiting_message.delete()
        except: pass
        return
    
    parsed_predict_data = await get_parsed_predict(predict_data)
    if not parsed_predict_data:
        await callback.message.answer('<b>Ошибка генерации</b>', reply_markup=filter_kb)
        try: await waiting_message.delete()
        except: pass
        return
    
    try: await waiting_message.delete()
    except: pass

    await callback.message.answer(f'<b>{predict_data[0]} - {predict_data[1]}\nНачало: {predict_data[3]} {predict_data[2]}\nПрогноз: {predict_data[5]} - КФ{predict_data[4]}</b>\n\n<i>{parsed_predict_data}</i>')


@user_router.callback_query(F.data == 'sport')
async def sport_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('<b>Выберите вид спорта</b>', reply_markup=choose_sport_kb)


@user_router.callback_query(F.data.startswith('sport_'))
async def filter_sport_handler(callback: CallbackQuery):
    await callback.answer()

    await edit_user_predict_filter(callback.message.chat.id, 'sport', callback.data.split('_')[1])
    
    predict_filter = await get_user_predict_filter(callback.message.chat.id)
    predict_filter = replace_filter_title(predict_filter)
    
    await callback.message.edit_text(f'<b>Можете выбрать фильтр для прогноза\n\nСпорт: {predict_filter["sport"]}\nКоэффициент: {predict_filter["k"][0]}-{predict_filter["k"][1]}\nДата: {predict_filter["date"]}</b>',
                            reply_markup=filter_kb)


@user_router.callback_query(F.data == 'k')
async def k_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('<b>Выберите коэффициент</b>', reply_markup=k_kb)


@user_router.callback_query(F.data.startswith('k_'))
async def filter_k_handler(callback: CallbackQuery):
    await callback.answer()

    await edit_user_predict_filter(callback.message.chat.id, 'k', [callback.data.split('_')[1], callback.data.split('_')[2]])
    
    predict_filter = await get_user_predict_filter(callback.message.chat.id)
    predict_filter = replace_filter_title(predict_filter)
    
    await callback.message.edit_text(f'<b>Можете выбрать фильтр для прогноза\n\nСпорт: {predict_filter["sport"]}\nКоэффициент: {predict_filter["k"][0]}-{predict_filter["k"][1]}\nДата: {predict_filter["date"]}</b>',
                            reply_markup=filter_kb)


@user_router.callback_query(F.data == 'date')
async def date_handler(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.edit_text('<b>Выберите дату</b>', reply_markup=date_kb)


@user_router.callback_query(F.data.startswith('date'))
async def filter_date_handler(callback: CallbackQuery):
    await callback.answer()
    
    await edit_user_predict_filter(callback.message.chat.id, 'date', callback.data.split('_')[1])
    
    predict_filter = await get_user_predict_filter(callback.message.chat.id)
    predict_filter = replace_filter_title(predict_filter)
    
    await callback.message.edit_text(f'<b>Можете выбрать фильтр для прогноза\n\nСпорт: {predict_filter["sport"]}\nКоэффициент: {predict_filter["k"][0]}-{predict_filter["k"][1]}\nДата: {predict_filter["date"]}</b>',
                            reply_markup=filter_kb)