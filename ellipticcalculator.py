from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty, ListProperty
from kivy.storage.dictstore import DictStore

from tools import elliptic_tools

Builder.load_string(open("kv/ellipticcalculator.kv", encoding='utf-8').read())

store = DictStore("elliptic.data")


class PatternTextInput(TextInput):
    multiline = False
    use_bubble = True
    name = StringProperty('')
    pat = StringProperty('')
    border_color = ListProperty((1, .1, .1, 0))
    created = False

    def delete_selection(self):
        if self.pat:
            return super(PatternTextInput, self).delete_selection()

    def do_backspace(self):
        if self.pat:
            return super(PatternTextInput, self).do_backspace()

    def on_text(self, instance, text):
        if self.created:
            if self.name and self.pat:
                store.put(self.name, value=text)
        else:
            if store.exists(self.name):
                self.text = store.get(self.name)['value']
            self.created = True

    def copy(self, data=''):
        Clipboard.copy(self.selection_text)

    def cut(self):
        self.copy()
        self.delete_selection()

    def paste(self):
        if self.pat:
            data = Clipboard.paste()
            text = self.text
            x = self.cursor[0]
            lenght = len(self.text) - x
            self.text = text[:x] + data + text[x:]
            self.cursor = (len(self.text) - lenght, self.cursor[1])

    def insert_text(self, substring, from_undo=False):
        if substring not in self.pat:
            substring = ''
        return super(PatternTextInput, self).insert_text(substring, from_undo=from_undo)


class EllipticCalculator(BoxLayout):
    colors = {'default': (1, 1, 1, 0),
              'error': (1, 0, 0, .8)}

    def calculate(self):
        self.default_all()

        if not self.curve_data.text or not self.entry.text:
            return

        curve = elliptic_tools.parse_curve_data(self.curve_data.text)

        if not curve:
            self.error(self.curve_data)
            return

        try:
            result = elliptic_tools.calculate(self.entry.text, curve)
        except Exception as e:
            self.error(self.entry)
            return
        else:
            if not result:
                self.error(self.entry)
                return

        self.result.text = str(result)

    def error(self, instance):

        instance.border_color = self.colors['error']

    def default_all(self):
        self.result.text = ''
        self.result.hint_text = 'Результат'

        self.curve_data.border_color = self.colors['default']
        self.entry.border_color = self.colors['default']
