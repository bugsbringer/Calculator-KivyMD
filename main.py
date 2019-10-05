__version__ = '0.3.5'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.theming import ThemeManager

from custom.button import CustomFlatIconButton

from update import Update

try:
    import android
except ImportError:
    android = None

if not android:
    W = 335
    Window.size = (W, W * 15.471074 / 9) #15.471074 / 9 соотношение сторон не фулскрин приложения на андроид


class Tab(CustomFlatIconButton):
    index = NumericProperty(0)
    bottom_line_color = ListProperty((1, 1, 1, 0))


class TabsBar(BoxLayout):
    __events__ = ('on_switch_tab',)
    current_tab = NumericProperty(0)

    def on_create(self):
        for i, tab in enumerate(self.children[::-1]):
            tab.index = i

        self.color_control()

    def switch_tab(self, index):
        self.current_tab = index

        self.color_control()

        self.dispatch('on_switch_tab')

    def on_switch_tab(self):
        pass

    def color_control(self):
        for tab in self.children:
            if tab.index == self.current_tab:
                tab.bottom_line_color[3] = .8
            else:
                tab.bottom_line_color[3] = 0


class MySettings(Screen):
    pass


class Calculator(Screen):

    def switch_screen(self, index):
        screen = self.scr_mang.screen_names[index]
        self.scr_mang.current = screen


class MainFrame(ScreenManager):

    def switch_screen(self, index):
        screen = self.scr_mang.screen_names[index]
        self.scr_mang.current = screen


class CalculatorApp(App):
    title = 'Calculator'
    theme_cls = ThemeManager()
    theme_cls.theme_style = 'Dark'

    color_scheme = {
        'button':           (.6, .56, 1, .25),
        'keyboard-button':  (.9, .85, 1, .05),
        'toolbar':          (.6, .56, 1, .25),
    }

    version = __version__
    git_version = ''
    update_available = False

    def build(self):
        update = Update(self, Window)
        update.start()
        return Builder.load_string(open("kv/main.kv", encoding='utf-8').read())

    def on_pause(self):
        return True


if __name__ == '__main__':
    CalculatorApp().run()
