from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

        self.aboutText = MDLabel()
        self.aboutText.text = "Бюджет производства: 3 копейки"
        self.aboutText.halign = "center"

        self.backButton = MDRaisedButton()
        
        self.backButton.text = "Назад"
        self.backButton.pos_hint = {"center_x": 0.5, "center_y": 0.1}
        self.backButton.size_hint = [0.75, 0.08]
        self.backButton.md_bg_color = [0, 0.75, 0.30, 1]
        self.backButton.font_size = 17

        self.add_widget(self.aboutText)
        self.add_widget(self.backButton)