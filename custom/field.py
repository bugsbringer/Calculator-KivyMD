from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty, NumericProperty

Builder.load_string('''
#:import TextfieldLabel kivymd.textfields.TextfieldLabel
<ScrollLabel>:
    scroller: scroller
    text_field: text_field

    on_text:
        text_field.text = self.text
        root.font_size_scale()

    ScrollView:
        id: scroller
        scroll_x: 1
        size_hint: None, 1
        width: root.text_field.size[0]

        TextfieldLabel:
            id: text_field
            valign: 'center'
            size_hint_x: None

            theme_text_color: 'Primary'

            size: self.texture_size[0], self.height
            text_size: None, self.texture_size[1]
            font_size: root.font_size

            on_size:
                root.scroll_sizer()
''')


class ScrollLabel(AnchorLayout):
    text = StringProperty()
    font_size = NumericProperty(36)
    scale_params = (None, None)  # (int, .percent)

    def font_size_scale(self):
        if self.scale_params != (None, None):
            min_len, min_size = self.scale_params

            lenght = len(self.text_field.text)

            self.text_field.font_size = self.text_field.height

            if lenght > min_len:
                for i in range(lenght - min_len):
                    self.text_field.font_size -= self.text_field.height * .05
                    if self.text_field.font_size < self.text_field.height * min_size:
                        self.text_field.font_size = self.text_field.height * min_size
                        break

    def scroll_sizer(self):
        if self.text_field.size[0] > self.size[0]:
            setattr(self.scroller, 'width', self.size[0])
        else:
            setattr(self.scroller, 'width', self.text_field.size[0])
