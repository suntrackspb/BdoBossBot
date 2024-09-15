from .bosses import router as boss_router
from .users import router as user_router
from .notification import router as notify_router
from .promocodes import router as promo_code_router


__all__ = [
    'boss_router',
    'user_router',
    'notify_router',
    'promo_code_router'
]
