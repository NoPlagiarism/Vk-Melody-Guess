from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import AsyncImage

from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip

Window.size = (350, 700)

# Имя + фамилия пользователя, нужно будет доставать с VK_API:
usernameData = "Иван Иванов"

# URL на аватарку:
avatarUrl = "https://dmitrovipoteka.ru/wp-content/uploads/2016/09/default-user-img.jpg"

# Соотношение по Y-оси с которой будет вести отчет блок управления (кнопки: Начать играть, Выход, Об игре):
controlPanelBlockStart = 0.40

# Соотношение по Y-оси с которой будет вести отчет блок с информацией (Аватарка, ФИ):
informationBlockStart = 0.75

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        self.username = MDLabel()

        self.username.text = usernameData
        self.username.pos_hint = {"center_y": informationBlockStart}
        self.username.font_size = 20
        self.username.halign = "center"

        self.avatar = AsyncImage(source = avatarUrl)

        self.avatar.size_hint = [0.35, 0.35]
        self.avatar.pos_hint = {"center_x": 0.5, "center_y": informationBlockStart - 0.135}

        self.tracksCount = MDChip()
        self.tracksCount.label = "Нет аудиозаписей"
        self.tracksCount.icon = ""
        self.tracksCount.pos_hint = {"center_x": 0.5, "center_y": informationBlockStart - 0.268}

        self.startToPlay = MDRaisedButton()
        self.exitFromAccount = MDRaisedButton()
        self.aboutGame = MDRaisedButton()

        self.startToPlay.text = "Начать играть"
        self.exitFromAccount.text = "Выход"
        self.aboutGame.text = "Об игре"

        self.startToPlay.pos_hint = {"center_x": 0.5, "center_y": controlPanelBlockStart}
        self.exitFromAccount.pos_hint = {"center_x": 0.305, "center_y": controlPanelBlockStart - 0.07}
        self.aboutGame.pos_hint = {"center_x": 0.695, "center_y": controlPanelBlockStart - 0.07}

        self.startToPlay.md_bg_color = [0, 0.75, 0.30, 1]
        self.exitFromAccount.md_bg_color = [0.93, 0.26, 0.26, 1]
        self.aboutGame.md_bg_color = [0.3, 0.3, 0.3, 1]

        self.startToPlay.size_hint = [0.75, 0.08]
        self.exitFromAccount.size_hint = [0.36, 0.04]
        self.aboutGame.size_hint = [0.36, 0.04]

        self.startToPlay.font_size = 17

        self.add_widget(self.username)
        self.add_widget(self.avatar)
        self.add_widget(self.tracksCount)
        self.add_widget(self.startToPlay)
        self.add_widget(self.exitFromAccount)
        self.add_widget(self.aboutGame)