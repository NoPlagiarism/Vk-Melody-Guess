from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton

blockStart = 0.6

class AuthScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthScreen, self).__init__(**kwargs)

        self.vkLogo = Image(source = "assets/vk_logo.png")
        self.vkLogo.size_hint = [0.25, 0.25]
        self.vkLogo.pos_hint = {"center_x": 0.5, "center_y": 0.8}

        self.loginInput = MDTextField()
        self.passInput = MDTextField()

        self.passInput.password = True
        self.passInput.required = True
        self.loginInput.required = True

        self.loginInput.helper_text_mode = "on_error"
        self.loginInput.helper_text = "Введите номер телефона или email"

        self.passInput.helper_text_mode = "on_error"
        self.passInput.helper_text = "Введите пароль"

        self.loginInput.hint_text = "Телефон или email"
        self.passInput.hint_text = "Пароль"

        self.loginInput.pos_hint = {"center_x": 0.5, "center_y": blockStart}
        self.passInput.pos_hint = {"center_x": 0.5, "center_y": blockStart - 0.07}

        self.loginInput.size_hint_x = 0.8
        self.passInput.size_hint_x = 0.8

        self.enterButton = MDRaisedButton()
        self.enterButton.text = "Войти"
        self.enterButton.pos_hint = {"center_x": 0.5, "center_y": blockStart - 0.20}
        self.enterButton.md_bg_color = [0, 0.75, 0.30, 1]
        self.enterButton.size_hint = [0.75, 0.08]
        self.enterButton.font_size = 17

        self.add_widget(self.vkLogo)
        self.add_widget(self.loginInput)
        self.add_widget(self.passInput)
        self.add_widget(self.enterButton)