from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from parser import get_predict_data
from keyboards.user_kbs import filrer_kb, choose_sport_kb, k_kb
from database.cruds import create_user_if_not_exists, get_user_predict_filter, edit_user_predict_filter


user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: Message):
    await create_user_if_not_exists(message.from_user.id)
    await message.answer('Hello, Im a bet-predict bot!')


@user_router.message(Command('predict'))
async def predict_handler(message: Message):
    predict_filter = await get_user_predict_filter(message.from_user.id)
    await message.answer(f'Можете выбрать фильтр для прогноза\n\nСпорт: {predict_filter["sport"]}\nКоэффициент: {predict_filter["k"]}\nДата: {predict_filter["date"]}',
                            reply_markup=filrer_kb)


@user_router.callback_query(F.data == 'get_predict')
async def get_predict_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    predict_filter = await get_user_predict_filter(callback.from_user.id)
    predict_data = await get_predict_data(predict_filter)
    await callback.message.answer(predict_data)


@user_router.callback_query(F.data == 'sport')
async def sport_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Выберите вид спорта', reply_markup=choose_sport_kb)


@user_router.callback_query(F.data.startswith('sport_'))
async def filter_sport_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text()
    await edit_user_predict_filter(callback.message.chat.id, 'sport', callback.data.split('_')[1])
    
    predict_filter = await get_user_predict_filter(callback.message.chat.id)
    await callback.message.answer(f'Можете выбрать фильтр для прогноза\n\nСпорт: {predict_filter["sport"]}\nКоэффициент: {predict_filter["k"]}\nДата: {predict_filter["date"]}',
                            reply_markup=filrer_kb)


@user_router.callback_query(F.data == 'k')
async def k_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите коэффициент', reply_markup=k_kb)


@user_router.callback_query(F.data.startswith('k_'))
async def filter_k_handler(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text()
    await edit_user_predict_filter(callback.message.chat.id, 'k', [callback.data.split('_')[1], callback.data.split('_')[2]])
