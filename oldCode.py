from kivy.app import App
from kivy.uix.button import Button


class LanguageLearnerApp(App):
    def build(self):
        return Button(
            text='Hello World',
            pos=(50, 50),
            size_hint=(0.32, 0.2)
            )


if __name__ == '__main__':
    LanguageLearnerApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
