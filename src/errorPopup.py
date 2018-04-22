__all__ = 'ErrorPopup'

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup

Builder.load_file('../res/kvs/errorPopup.kv')


class ErrorPopup(Popup):
    ErrorHeader = StringProperty('<Error Head>')
    ErrorMsg = StringProperty('')

    def __init__(self, header=None, msg=None, **kwargs):
        super().__init__(**kwargs)
        if header:
            self.ErrorHeader = header
        if msg:
            self.ErrorMsg = msg

    def set_header(self, header):
        self.ErrorHeader = header

    def set_message(self, msg):
        self.ErrorMsg = msg
