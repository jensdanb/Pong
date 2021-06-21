import os
os.environ['KIVY_TEXT'] = 'pil'
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty


# Elements here, aka. child and intermediate widgets
class WidgetGenerator(Button):
    pass


class MyWidget(Widget):
    pass


# Architecture; aka. root widget
class WorkSpace(Widget):
    def __init__(self, **kwargs):
        super(WorkSpace, self).__init__(**kwargs)
        # widget_generator = ObjectProperty()


class TemplateApp(App):
    def build(self):
        workspace = WorkSpace()

        return workspace


if __name__ == '__main__':
    TemplateApp().run()