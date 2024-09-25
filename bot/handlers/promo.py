import re
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from common.schemas.promocodes import PromoCodeSchema
from bot.keyboards.inline import add_promo_code_keyboard
from bot.keyboards.reply import main_keyboard
from bot.states.promocodes import AddPromoStates
from bot.utils.constants import BotButtons
from bot.utils.functions import format_promo_message
from bot.utils.http_client import HttpClient

router = Router()


@router.message(F.text == BotButtons.PROMO.value)
async def notify(message: Message, **middlewares):
    client: HttpClient = middlewares.get('client')
    request = await client.get_promos()
    promo_list = [PromoCodeSchema(**promo) for promo in request.data]
    return await message.answer(format_promo_message(promo_list), reply_markup=add_promo_code_keyboard())


@router.callback_query(F.data == "add_promo_code")
async def add_code(callback: CallbackQuery, state: FSMContext, **middlewares):
    await state.set_state(AddPromoStates.enter_promo)
    await callback.message.edit_text("Введи код купона в формате: <b>XXXX-XXXX-XXXX-XXXX</b>")
    await callback.answer()


@router.message(AddPromoStates.enter_promo)
async def add_code(message: Message, state: FSMContext, **middlewares):
    if re.search(r'^[!A-Z0-9]{4}(-[!A-Z0-9]{4}){2,3}$', message.text.strip()) is None:
        return await message.answer('Не правильный формат купона!', reply_markup=add_promo_code_keyboard())
    await state.update_data(code=message.text)
    client: HttpClient = middlewares.get('client')
    request = await client.check_promo(message.text)
    print(request)
    if request.status_code == 200:
        promo = PromoCodeSchema(**request.data)
        return await message.answer(f"КУПОН УЖЕ СУЩЕСТВУЕТ!\n\n{format_promo_message([promo])}",
                                    reply_markup=add_promo_code_keyboard())
    elif request.status_code == 404:
        await state.set_state(AddPromoStates.enter_expire)
        await message.answer("Введи дату окончания купона в формате: <b>YYYY-MM-DD HH:MM</b>")
    else:
        return await message.answer(f'{request.status_code} {request.message}')


@router.message(AddPromoStates.enter_expire)
async def add_expire(message: Message, state: FSMContext, **middlewares):
    if re.search(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', message.text.strip()) is None:
        return await message.answer('Не правильный формат даты!', reply_markup=add_promo_code_keyboard())
    expire = datetime.strptime(message.text, '%Y-%m-%d %H:%M')
    await state.update_data(expire=expire)
    await state.set_state(AddPromoStates.enter_loot)
    return await message.answer("Введи содержимое купона, например:"
                                "\n<i>Свиток удачи\nСундук помощи в усилении\n[Ивент] Сундук помощи III</i>")


@router.message(AddPromoStates.enter_loot)
async def add_loot(message: Message, state: FSMContext, **middlewares):
    await state.update_data(owner=message.from_user.id)
    await state.update_data(created_at=datetime.now())
    await state.update_data(loot=message.text)
    client: HttpClient = middlewares.get('client')
    state_data = await state.get_data()
    request = await client.add_promo(
        PromoCodeSchema(**state_data)
    )
    if request.status_code == 200:
        return await message.answer(
            "Спасибо, купон будет проверен модератором и добавлен в базу.",
            reply_markup=main_keyboard()
        )
    else:
        return await message.answer(f'{request.status_code} {request.message}')
