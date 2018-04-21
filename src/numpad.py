__all__ = 'NumbPad'

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_file('numpad.kv')


class Numpad(GridLayout):
    pass
