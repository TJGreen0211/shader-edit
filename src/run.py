from kivy.config import Config

from math import cos, sin, radians, exp
from kivy.core.window import Window  # noqa
from kivy.lang import Builder
from kivy.properties import AliasProperty, DictProperty, ListProperty
from kivy.clock import Clock, mainthread
from kivy.app import App

KV = '''
#:import listdir os.listdir
#:import A kivy.animation.Animation
<Button>:
    font_name: '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FloatLayout:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: 48
            Label:
                text: 'x: '
            Label:
                text: 'y: '
            Label:
                text: 'z: '
            Label:
                text: 'rx: '
            Label:
                text: 'ry: '
            Label:
                text: 'rz: '
            Label:
                size_hint_x: None
                width: self.texture_size[0]
                text: 'vec: '
            Label:
                text: ''
'''  # noqa

class App3D(App):
    def build(self):
        root = Builder.load_string(KV)
        return root

def run():
    App3D().run()


if __name__ == '__main__':
    run()