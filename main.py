import threading
import credits

import screens
import vkapi

from vk_api import VkApi

from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.app import MDApp

class Main(MDApp):
    def aboutGamePressed(self, instance):
        self.screenManagment.transition.direction = "left"
        self.startScreen.manager.current = "about"

    def backFromAboutPressed(self, instance):
        self.screenManagment.transition.direction = "right"
        self.aboutScreen.manager.current = "start"

    def initializeTracksCount(self):
        session = VkApi(credits.login, credits.password)
        session.auth()

        audio = vkapi.audio(session)
        tracksCount = audio.get_len_user_audio()

        if tracksCount != 0:
            self.startScreen.tracksCount.label = "Аудиозаписей: " + str(tracksCount)
        else:
            self.startScreen.tracksCount.label = "Нет аудиозаписей"

    def build(self):
        initThread = threading.Thread(target = self.initializeTracksCount)
        initThread.start()

        self.screenManagment = ScreenManager(transition = SlideTransition())

        self.startScreen = screens.start(name = "start")
        self.aboutScreen = screens.about(name = "about")

        self.startScreen.aboutGame.bind(on_press = self.aboutGamePressed)
        self.aboutScreen.backButton.bind(on_press = self.backFromAboutPressed)

        self.screenManagment.add_widget(self.startScreen)
        self.screenManagment.add_widget(self.aboutScreen)

        return self.screenManagment

if __name__ == '__main__':
    Main().run()