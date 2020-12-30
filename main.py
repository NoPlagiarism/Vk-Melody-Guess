import threading
import time
import urllib.request

import screens
import vkapi

from vk_api import VkApi

from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.lang import Builder
from kivymd.app import MDApp
from random import randint, random

class Main(MDApp):
    def aboutGamePressed(self, instance):
        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "about"

    def backFromAboutPressed(self, instance):
        self.screenManagement.transition.direction = "right"
        self.screenManagement.current = "start"

    def authHandler(self):
        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "two_factor"
        
        while not self.twoFactorScreen.buttonPressed:
            time.sleep(0.2)
            continue

        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "loading"

        return self.twoFactorScreen.keyInput.text, True

    def captchaHandler(self, captcha):
        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "loading"

        urllib.request.urlretrieve(captcha.get_url(), "gifs/captcha.jpg")
        self.captchaScreen.captcha.source = "gifs/captcha.jpg"

        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "captcha"

        while not self.captchaScreen.buttonPressed:
            time.sleep(0.2)
            continue

        return captcha.try_again(self.captchaScreen.keyInput.text)

    def initializeTracksCount(self):
        session = VkApi(self.authScreen.loginInput.text, 
            self.authScreen.passInput.text, auth_handler = self.authHandler,
            captcha_handler = self.captchaHandler)

        try:
            session.auth(reauth = True)
        except Exception as ex:
            self.screenManagement.transition.direction = "left"
            self.screenManagement.current = "auth"

            print(ex)

            return

        audio = vkapi.audio(session)
        self.tracksCount = audio.get_len_user_audio()

        if self.tracksCount != 0:
            self.startScreen.tracksCount.label = "Аудиозаписей: " + str(self.tracksCount)
        else:
            self.startScreen.tracksCount.label = "Нет аудиозаписей"
        
        user = session.method("users.get", {"user_ids": audio.user_id, "fields": "photo_200"})
        
        self.startScreen.username.text = user[0]["first_name"] +  ' ' + user[0]["last_name"]
        self.startScreen.avatar.source = user[0]["photo_200"]

        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "start"

    def enterButtonPressed(self, instance):
        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "loading"

        initThread = threading.Thread(target = self.initializeTracksCount)
        initThread.start()

    def twoFactorButtonPressed(self, instance):
        self.twoFactorScreen.buttonPressed = True

    def captchaButtonPressed(self, instance):
        self.captchaScreen.buttonPressed = True
    
    def exitButtonPressed(self, instance):
        self.captchaScreen.captcha.source = ""
        self.captchaScreen.keyInput.text = ""
        self.twoFactorScreen.keyInput.text = ""

        self.captchaScreen.buttonPressed = False
        self.twoFactorScreen.buttonPressed = False

        self.startScreen.username.text = "Не определено"
        self.startScreen.avatar.source = "https://vk.com/images/camera_200.png?ava=1"

        self.authScreen.loginInput.text = ""
        self.authScreen.passInput.text = ""
        self.tracksCount = 0

        self.screenManagement.transition.direction = "right"
        self.screenManagement.current = "auth"

    def check_song(self, _):
        self.screenManagement.current = "result"
        self.resultScreen("Сто баксов", "Дикая деревня", (bool(random()), bool(random())))
        t = threading.Thread(target=self.wait_and_change)
        t.start()

    def wait_and_change(self):
        time.sleep(3)
        self.overScreen(randint(0, 360))
        self.screenManagement.current = "over"

    def startGamePressed(self, instance):
        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "game"

    def backButtonPressed(self, instance):
        self.screenManagement.current = "start"

    def build(self):
        self.screenManagement = ScreenManager(transition = SlideTransition())

        Builder.load_string(screens.game_helper)

        self.gameScreen = screens.game()
        self.resultScreen = screens.result()
        self.overScreen = screens.over()

        self.gameScreen.init_binds(self.check_song)
        self.overScreen.back_btn.bind(on_press = self.backButtonPressed)
        
        self.authScreen = screens.auth(name = "auth")
        self.twoFactorScreen = screens.two_factor(name = "two_factor")
        self.captchaScreen = screens.captcha(name = "captcha")
        self.loadingScreen = screens.loading(name = "loading")
        self.startScreen = screens.start(name = "start")
        self.aboutScreen = screens.about(name = "about")

        self.twoFactorScreen.enterButton.bind(on_press = self.twoFactorButtonPressed)
        self.authScreen.enterButton.bind(on_press = self.enterButtonPressed)
        self.captchaScreen.enterButton.bind(on_press = self.captchaButtonPressed)
        self.startScreen.aboutGame.bind(on_press = self.aboutGamePressed)
        self.startScreen.exitFromAccount.bind(on_press = self.exitButtonPressed)
        self.startScreen.startToPlay.bind(on_press = self.startGamePressed)
        self.aboutScreen.backButton.bind(on_press = self.backFromAboutPressed)

        self.screenManagement.add_widget(self.authScreen)
        self.screenManagement.add_widget(self.twoFactorScreen)
        self.screenManagement.add_widget(self.captchaScreen)
        self.screenManagement.add_widget(self.loadingScreen)
        self.screenManagement.add_widget(self.startScreen)
        self.screenManagement.add_widget(self.aboutScreen)
        self.screenManagement.add_widget(self.gameScreen)
        self.screenManagement.add_widget(self.resultScreen)
        self.screenManagement.add_widget(self.overScreen)

        return self.screenManagement

if __name__ == "__main__":
    Main().run()