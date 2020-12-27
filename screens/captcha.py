from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton

blockStart = 0.6

class CaptchaScreen(Screen):
    def __init__(self, **kwargs):
        super(CaptchaScreen, self).__init__(**kwargs)

        self.buttonPressed = False

        self.captcha = Image()
        self.captcha.size_hint = [0.25, 0.25]
        self.captcha.pos_hint = {"center_x": 0.5, "center_y": 0.8}

        self.keyInput = MDTextField()

        self.keyInput.required = True
        self.keyInput.helper_text_mode = "on_error"
        self.keyInput.helper_text = "Введите код подтверждения входа"

        self.keyInput.hint_text = "Код подтверждения входа"
        self.keyInput.pos_hint = {"center_x": 0.5, "center_y": blockStart}
        self.keyInput.size_hint_x = 0.8

        self.enterButton = MDRaisedButton()
        self.enterButton.text = "Войти"
        self.enterButton.pos_hint = {"center_x": 0.5, "center_y": blockStart - 0.20}
        self.enterButton.md_bg_color = [0, 0.75, 0.30, 1]
        self.enterButton.size_hint = [0.75, 0.08]
        self.enterButton.font_size = 17

        self.add_widget(self.captcha)
        self.add_widget(self.keyInput)
        self.add_widget(self.enterButton)