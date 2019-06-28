from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout

from kivymd.button import MDFlatButton

from custom.button import LongPressButton

from tools.calculation import calculate

Builder.load_string(open("kv/usual.kv", encoding='utf-8').read())


class MultiModeFlatButton(LongPressButton, MDFlatButton):
    modes = ListProperty(['', ''])
    mode = 0

    def on_long_press(self):
        self.mode = (self.mode + 1) % len(self.modes)
        self.text = self.modes[self.mode]
        super(MultiModeFlatButton, self).on_long_press()


class StoryRow(BoxLayout):
    text = StringProperty("")
    result = StringProperty("")


class Story(ScrollView):

    def copybody(self, instance):
        self.parent.parent.enter_number(instance)

    def copy(self, instance):
        result_instance = StoryRow(text=instance.result)
        self.parent.parent.enter_number(result_instance)

    def push(self, text, result):
        if text and result:
            self.container.add_widget(StoryRow(text=text, result=result,
                                                height=self.height / 3))

    def clear(self):
        self.container.clear_widgets()


class UsualCalculator(BoxLayout):
    entry_status = '0'
    ignored_items = ['0', 'Ошибка','Простое число']
    functions = ['НОД', 'НОК', 'φ', 'F']
    operations = ['+', '-', '÷', '×', ',', '^', 'mod ']

    def enter_operation(self, instance):
        self.entry_status = self.entry.text

        if self.entry_status in self.ignored_items or self.entry_status is '-':
            self.entry_status = ''

        buffer = instance.text
        buffer = buffer.replace('mod', ' mod ')
        buffer = buffer.replace('x-¹', '-¹mod ')

        if buffer == ',':
            left = self.entry_status.count('(')
            right = self.entry_status.count(')')
            if left - right == 0:
                buffer = ''

        lngh = len(self.entry_status)
        if self.entry_status[lngh - 1:] == '.':
            self.entry_status += '0'

        lngh = len(self.entry_status)
        for oprtn in self.operations:
            if self.entry_status[lngh - len(oprtn):] == oprtn:
                self.backspace()
                break

        lngh = len(self.entry_status)
        if self.entry_status[lngh - 1:] is '(':
            if buffer is '-':
                self.entry_status += buffer
        elif self.entry_status or buffer is '-':
            self.entry_status += buffer

        self.refresh_entry()

    def enter_number(self, instance):
        if self.entry_status in self.ignored_items:
            self.entry_status = ''

        buffer = instance.text
        buffer = buffer.replace('F(N)', 'F')
        buffer = buffer.replace('φ(x)', 'φ')

        lngh = len(self.entry_status)

        if instance.text == '.':
            if lngh == 0:
                buffer = '0.'
            else:
                if self.entry_status[lngh - 1].isdigit():
                    for i in range(lngh - 2, -1, -1):
                        if not self.entry_status[i: lngh - 1].isdigit():
                            if self.entry_status[i] == '.':
                                buffer = ''
                            break

                else:
                    buffer = ''
                    if self.entry_status[lngh - 1] == '.':
                        buffer = '0.'

        elif buffer in self.functions:
            if self.entry_status and self.entry_status[lngh - 1].isdigit():
                buffer = '×' + buffer + '('

            else:
                buffer = '' + buffer + '('

        if lngh > 0 and self.entry_status[lngh - 1] == ')':
            self.entry_status += '×'

        self.entry_status += buffer

        self.refresh_entry()

    def parentheses(self):
        if self.entry_status in self.ignored_items:
            self.entry_status = ''

        buffer = ''
        left = self.entry_status.count('(')
        right = self.entry_status.count(')')
        lngh = len(self.entry_status)

        if not self.entry_status:
            buffer = '('

        elif self.entry_status[lngh - 1].isdigit():
            if left - right > 0:
                buffer = ')'
            else:
                buffer = '×('

        elif self.entry_status[lngh - 1] == ')':
            if left - right == 0:
                buffer = '×('
            else:
                buffer = ')'

        else:
            buffer = '('

        self.entry_status += buffer

        self.refresh_entry()

    def result(self):
        left = self.entry_status.count('(')
        right = self.entry_status.count(')')
        self.entry_status += ')' * (left - right)

        self.refresh_entry()

        result = calculate(self.entry_status)

        if type(result) is float:
            result = round(result, 6)

        self.entry_status = str(result)

        if self.entry_status != self.entry.text:
            if self.entry_status != 'Ошибка':
                self.story.push(self.entry.text, self.entry_status)
            self.refresh_entry()

            self.entry_status = '0'

    def clear(self):
        if self.entry.text == '0':
            self.story.clear()
        else:
            self.entry_status = '0'
            self.refresh_entry()

    def backspace(self):
        lngh = len(self.entry_status)
        long_items = ['-¹mod ', ' mod ', 'НОД(', 'НОК(', 'φ(', 'pow(', 'F(']

        for item in long_items:
            if self.entry_status[lngh - len(item):] == item:
                self.entry_status = self.entry_status[:lngh - len(item)]
                self.refresh_entry()
                return

        self.entry_status = self.entry_status[:lngh - 1]

        self.refresh_entry()

    def refresh_entry(self):
        if self.entry_status == '': # or self.entry_status == '()'
            self.entry_status = '0'

        self.entry.text = self.entry_status
