# scrapers/__init__.py
from .rema import get_price as rema_get_price
from .kiwi import get_price as kiwi_get_price
from .meny import get_prices as meny_get_prices  # meny uses get_prices, not get_price

