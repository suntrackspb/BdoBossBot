from datetime import datetime, timedelta
from typing import List

from common.schemas.promocodes import PromoCodeSchema


def declension(number, words):
    if 11 <= number % 100 <= 14:
        return f"{number} {words[2]}"
    elif number % 10 == 1:
        return f"{number} {words[0]}"
    elif 2 <= number % 10 <= 4:
        return f"{number} {words[1]}"
    else:
        return f"{number} {words[2]}"


def down_counter(date_str):
    if date_str == '00:00:00':
        date_str = '23:59:59'

    now = datetime.now()
    target_time = datetime.strptime(date_str, '%H:%M:%S').replace(
        year=now.year, month=now.month, day=now.day
    )

    if target_time < now:
        target_time += timedelta(days=1)

    check_time = (target_time - now).total_seconds()

    if check_time <= 0:
        return False

    days = int(check_time // 86400)
    hours = int((check_time % 86400) // 3600)
    minutes = int((check_time % 3600) // 60)
    seconds = int(check_time % 60)

    result = []
    if days > 0:
        result.append(declension(days, ['день', 'дня', 'дней']))
    if hours > 0:
        result.append(declension(hours, ['час', 'часа', 'часов']))
    if minutes > 0:
        result.append(declension(minutes, ['минута', 'минуты', 'минут']))
    if seconds > 0:
        result.append(declension(seconds, ['секунда', 'секунды', 'секунд']))

    return ' '.join(result)


def promo_counter(promo_expire: datetime):
    current_date = datetime.now()
    diff = promo_expire.replace(tzinfo=None) - current_date
    return declension(diff.days, ['день', 'дня', 'дней'])


def format_promo_message(promos: List[PromoCodeSchema]):
    items = []
    for promo in promos:
        expire = promo_counter(promo.expire)
        string = f'<code>{promo.code}</code>\n<i>Осталось: {expire}</i>\n\n'
        items.append(string)
    return ''.join(items)

