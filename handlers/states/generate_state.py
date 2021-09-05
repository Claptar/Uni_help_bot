from typing import Tuple
from aiogram.dispatcher.filters.state import State, StatesGroup


def generate_state(cls_name: str, names: Tuple[str]):
    return type(cls_name, (StatesGroup,), {name: State() for name in names})
