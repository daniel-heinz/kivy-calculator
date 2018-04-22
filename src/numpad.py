__all__ = 'NumbPad'

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_file('numpad.kv')


class Numpad(GridLayout):
    def __init__(self, calc_bar, **kwargs):
        super().__init__(**kwargs)
        self.calc_bar = calc_bar
