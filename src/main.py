from asteval import Interpreter
from kivy.app import App
from kivy.multistroke import Recognizer
from kivy.properties import StringProperty
from kivy.uix.gesturesurface import GestureSurface
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from errorPopup import ErrorPopup
from numpad import Numpad
from settings import CalculatorSettingsContainer


class CalcBar(GridLayout):
    calc_value = StringProperty('15')

    def clear_value(self):
        self.calc_value = ''

    def del_last(self):
        self.calc_value = self.calc_value[:-1]

    def update_display(self, symbol):
        if len(self.calc_value) != 0 and symbol == 'sqrt':
            self.calc_value = 'sqrt({0})'.format(self.calc_value)
        elif len(self.calc_value) != 0 and symbol == '()':
            self.calc_value = '({0})'.format(self.calc_value)
        else:
            self.calc_value += symbol

    def exec_calc(self):
        if len(self.calc_value) != 0:
            a_eval = Interpreter()
            res = str(a_eval(self.calc_value))

            if len(a_eval.error) > 0:
                err = a_eval.error[0].get_error()
                err_box = ErrorPopup()
                err_box.set_header('An {0} occurred.\nPleas check below for details.'.format(err[0]))
                err_list = [str(e.get_error()[1]).strip() + '\n' for e in a_eval.error]
                err_box.set_message(' '.join(err_list))
                err_box.open()
            else:
                self.calc_value = res


class MainMenu(GridLayout):
    pass


class CalculatorAppSettings(CalculatorSettingsContainer):
    pass


class CalculatorApp(App):

    def handle_gesture_cleanup(self, surface, g, *l):
        if hasattr(g, '_result_label'):
            surface.remove_widget(g._result_label)

    def handle_gesture_discard(self, surface, g, *l):
        if surface.draw_timeout == 0:
            return

        text = '[b]Discarded:[/b] Not enough input'
        g._result_label = Label(text=text, markup=True, size_hint=(None, None),
                                center=(g.bbox['minx'], g.bbox['miny']))
        self.surface.add_widget(g._result_label)

    def handle_gesture_complete(self, surface, g, *l):
        result = self.recognizer.recognize(g.get_vectors())
        result._gesture_obj = g
        result.bind(on_complete=self.handle_recognize_complete)

    def handle_recognize_complete(self, result, *l):
        if self.surface.draw_timeout == 0:
            return

        best = result.best
        if best['name'] is None:
            text = '[b]No match[/b]'
        else:
            text = 'Name: [b]%s[/b]\nScore: [b]%f[/b]\nDistance: [b]%f[/b]' % (
                   best['name'], best['score'], best['dist'])
            self.calc_bar.update_display(best['name'])

        g = result._gesture_obj
        g._result_label = Label(text=text, markup=True, size_hint=(None, None),
                                center=(g.bbox['minx'], g.bbox['miny']))
        self.surface.add_widget(g._result_label)

    def build(self):
        self.manager = ScreenManager(transition=SlideTransition(
                                     duration=.15))
        self.recognizer = Recognizer()
        self.recognizer.import_gesture(filename='./calc_symbols.kg')
        self.calc_bar = CalcBar()


        # Gesture screen
        surface = GestureSurface(line_width=2, draw_bbox=True,
                                 use_random_color=True)
        surface_screen = Screen(name='surface')
        surface_screen.add_widget(surface)
        self.manager.add_widget(surface_screen)

        surface.bind(on_gesture_discard=self.handle_gesture_discard)
        surface.bind(on_gesture_complete=self.handle_gesture_complete)
        surface.bind(on_gesture_cleanup=self.handle_gesture_cleanup)
        self.surface = surface

        # NumPad screen
        numpad = Numpad(self.calc_bar)
        numpad_screen = Screen(name='numpad')
        numpad_screen.add_widget(numpad)
        self.manager.add_widget(numpad_screen)

        # Settings screen
        app_settings = CalculatorAppSettings()
        ids = app_settings.ids

        ids.max_strokes.bind(value=surface.setter('max_strokes'))
        ids.temporal_win.bind(value=surface.setter('temporal_window'))
        ids.timeout.bind(value=surface.setter('draw_timeout'))
        ids.line_width.bind(value=surface.setter('line_width'))
        ids.draw_bbox.bind(value=surface.setter('draw_bbox'))
        ids.use_random_color.bind(value=surface.setter('use_random_color'))

        settings_screen = Screen(name='settings')
        settings_screen.add_widget(app_settings)
        self.manager.add_widget(settings_screen)

        # Wrap in a gridlayout so the main menu is always visible
        layout = GridLayout(cols=1)
        layout.add_widget(self.calc_bar)
        layout.add_widget(MainMenu())
        layout.add_widget(self.manager)
        return layout


if __name__ in ('__main__', '__android__'):
    CalculatorApp().run()
