from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from custom.button import LongPressButton
from kivy.uix.button import Button

Builder.load_string(open("kv/ellipticcalculator.kv", encoding='utf-8').read())



class EllipticCalculator(BoxLayout):
    pass

class CustomButton(LongPressButton, Button):
    pass
