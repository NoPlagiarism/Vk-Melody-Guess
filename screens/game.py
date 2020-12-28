from colorsys import hsv_to_rgb
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivymd.uix.slider import MDSlider as _MDSlider
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from random import randint, random
from time import sleep
import threading

game_helper = """
ScreenManager:
    GameScreen
    ResultScreen
    OverScreen
<GameScreen>:
    id: game
    name: "game"
    slider: slider
    track_field: track_field
    author_field: author_field
    check_btn: check_btn
    play_btn: play_btn
    stop_btn: stop_btn
    MDIconButton:
        id: play_btn
        icon: "play"
        pos_hint: {"center_x": .9,"center_y": .9}
    UnMDSlider:
        id: slider
        orientation: "horizontal"
        pos_hint: {"center_x": .5, "center_y": .85}
        size_hint_x: .7
        hint: False
        min: 0
        max: 235
        sensitivity: "handle"
        disabled: False
        cursor_disabled_image: "assets/cursor.png"
        value: 1
    MDIconButton:
        id: stop_btn
        icon: "stop"
        pos_hint: {"center_x": .1,"center_y": .9}
    MDLabel:
        text: root.score_str
        pos_hint: {"center_x": .5, "center_y": .9}
        font_size: "48dp"
        halign: "center"
    MDTextField:
        id: track_field
        hint_text: "Введите название песни"
        size_hint_x: .8
        pos_hint: {"center_x": .5, "center_y": .55}
    MDTextField:
        id: author_field
        hint_text: "Введите автора"
        size_hint_x: .8
        pos_hint: {"center_x": .5, "center_y": .45}
    MDRaisedButton:
        id: check_btn
        text: "Проверить"
        size_hint: (0.75, 0.08)
        font_size: 17
        pos_hint: {"center_x": .5,"center_y": .3}
<ResultScreen>:
    id: result
    name: "result"
    MDLabel:
        text: "0"
        pos_hint: {"center_x": .5, "center_y": .9}
        font_size: "48dp"
        halign: "center"
    MDLabel:
        text: root.track
        halign: "center"
        pos_hint: {"center_x": .5, "center_y": .55}
        font_size: "48 sp"
        color: root.track_color
    MDLabel:
        text: root.author
        halign: "center"
        pos_hint: {"center_x": .5, "center_y": .45}
        font_size: "32 sp"
        color: root.author_color
    MDLabel:
        text: "+1"
        halign: "center"
        font_size: "52 sp"
        pos_hint: {"center_x": .5, "center_y": .2}
        color: (0, .75, .30, 1)
<OverScreen>:
    id: over
    name: "over"
    back_btn: back_btn
    MDLabel:
        text: "Вы набрали"
        pos_hint: {"center_x": .5, "center_y": .7}
        font_size: "64 sp"
        halign: "center"
    MDLabel:
        text: root.score_str
        color: root.score_color
        pos_hint: {"center_x": .5, "center_y": .5}
        font_size: "150 sp"
        halign: "center"
    MDLabel:
        text: "баллов"
        pos_hint: {"center_x": .5, "center_y": .3}
        font_size: "64 sp"
        halign: "center"
    MDRaisedButton:
        id: back_btn
        text: "Вернуться в меню"
        size_hint: (0.75, 0.08)
        font_size: 17
        pos_hint: {"center_x": 0.5, "center_y": 0.1}
"""


class UnMDSlider(_MDSlider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        pass

    def on_touch_move(self, touch):
        pass


class GameScreen(MDScreen):
    score_str = StringProperty("0")
    slider = ObjectProperty(None)
    track_field = ObjectProperty(None)
    author_field = ObjectProperty(None)
    check_btn = ObjectProperty(None)
    play_btn = ObjectProperty(None)
    stop_btn = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

    def init_binds(self, btn_handler, play=lambda x: x, stop=lambda x: x):
        self.check_btn.bind(on_press=btn_handler)
        self.play_btn.bind(on_release=play)
        self.stop_btn.bind(on_release=stop)


class ResultScreen(MDScreen):
    score_str = StringProperty("1")
    score_delta = StringProperty("+1")
    track = StringProperty("")
    author = StringProperty("")
    track_color = ListProperty(defaultvalue=(0, 0, 0, 1))
    author_color = ListProperty(defaultvalue=(0, 0, 0, 1))
    COLORS = {True: (0, .75, .30, 1), False: (.93, .26, .26, 1)}

    def __call__(self, track: str, author: str, results):
        self.track = track
        self.author = author
        self.track_color = self.COLORS.get(results[0], (0, 0, 0, 1))
        self.author_color = self.COLORS.get(results[1], (0, 0, 0, 1))


class OverScreen(MDScreen):
    score_str = StringProperty("0")
    score_color = ListProperty((0, 0, 0, 1))
    back_btn = ObjectProperty(None)

    def __call__(self, score: int):
        self.score_str = str(score)
        if score > 300:
            score = 300
        self.score_color = (*hsv_to_rgb(score/360, 1, 1), 1)
