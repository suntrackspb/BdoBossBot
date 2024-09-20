from aiogram.fsm.state import StatesGroup, State


class AddPromoStates(StatesGroup):
    enter_promo = State()
    enter_expire = State()
    enter_loot = State()
