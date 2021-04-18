from kivy.app import App
from kivy.uix.button import Button


class FunkyButton(Button):
    def __init__(self, **kwargs):
        super(FunkyButton, self).__init__(**kwargs)
        self.text = "Hello there"
        self.pos = (100, 100)
        self.size_hint = (0.5, 0.4)


class LanguageLearnerApp(App):
    def build(self):
        return FunkyButton()


if __name__ == '__main__':
    LanguageLearnerApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
