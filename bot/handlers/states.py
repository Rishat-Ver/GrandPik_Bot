from aiogram.fsm.state import State, StatesGroup


class SearchStates(StatesGroup):
    waiting_for_search_input = State()


class AddStates(StatesGroup):
    waiting_for_add_input = State()