from aiogram.fsm.state import State, StatesGroup


class SearchStates(StatesGroup):
    waiting_for_search_input = State()


class AddStates(StatesGroup):
    waiting_for_add_input = State()


class DeleteStates(StatesGroup):
    waiting_for_delete_input = State()


class StatsStates(StatesGroup):
    waiting_for_stats_input = State()