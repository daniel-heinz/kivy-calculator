__all__ = ('CalculatorSettingsContainer', 'CalculatorSettingItem',
           'CalculatorSettingBoolean', 'CalculatorSettingSlider',
           'CalculatorSettingString', 'CalculatorSettingTitle')

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (StringProperty, NumericProperty, OptionProperty,
                             BooleanProperty)
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

Builder.load_file('../res/kvs/settings.kv')


class CalculatorSettingsContainer(GridLayout):
    pass


class CalculatorSettingItem(GridLayout):
    title = StringProperty('<No title set>')
    desc = StringProperty('')


class CalculatorSettingTitle(Label):
    title = StringProperty('<No title set>')
    desc = StringProperty('')


class CalculatorSettingBoolean(CalculatorSettingItem):
    button_text = StringProperty('')
    value = BooleanProperty(False)


class CalculatorSettingString(CalculatorSettingItem):
    value = StringProperty('')


class EditSettingPopup(Popup):
    def __init__(self, **kwargs):
        super(EditSettingPopup, self).__init__(**kwargs)
        self.register_event_type('on_validate')

    def on_validate(self, *l):
        pass


class CalculatorSettingSlider(CalculatorSettingItem):
    min = NumericProperty(0)
    max = NumericProperty(100)
    type = OptionProperty('int', options=['float', 'int'])
    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(CalculatorSettingSlider, self).__init__(**kwargs)
        self._popup = EditSettingPopup()
        self._popup.bind(on_validate=self._validate)
        self._popup.bind(on_dismiss=self._dismiss)

    def _to_numtype(self, v):
        try:
            if self.type == 'float':
                return round(float(v), 1)
            else:
                return int(v)
        except ValueError:
            return self.min

    def _dismiss(self, *l):
        self._popup.ids.input.focus = False

    def _validate(self, instance, value):
        self._popup.dismiss()
        val = self._to_numtype(self._popup.ids.input.text)
        if val < self.min:
            val = self.min
        elif val > self.max:
            val = self.max
        self.value = val

    def on_touch_down(self, touch):
        if not self.ids.sliderlabel.collide_point(*touch.pos):
            return super(CalculatorSettingSlider, self).on_touch_down(touch)
        ids = self._popup.ids
        ids.value = str(self.value)
        ids.input.text = str(self._to_numtype(self.value))
        self._popup.open()
        ids.input.focus = True
        ids.input.select_all()


Factory.register('CalculatorSettingsContainer',
                 cls=CalculatorSettingsContainer)
Factory.register('CalculatorSettingTitle', cls=CalculatorSettingTitle)
Factory.register('CalculatorSettingBoolean', cls=CalculatorSettingBoolean)
Factory.register('CalculatorSettingSlider', cls=CalculatorSettingSlider)
Factory.register('CalculatorSettingString', cls=CalculatorSettingString)

