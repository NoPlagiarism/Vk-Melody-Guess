import threading
import time
import urllib.request
import sys
import os
# import pythonforandroid.recipes.android as android

import screens
import vkapi

from vk_api import VkApi

from kivy.core.audio import SoundLoader
from kivy.clock import mainthread
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.lang import Builder
from kivymd.app import MDApp
from random import randint, choice
import audio as _audio


CACHE_PATH = "{0}\\cache\\".format(sys.path[0])


class MainApp(MDApp):
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
        self.vk = VkApi(self.authScreen.loginInput.text,
                        self.authScreen.passInput.text, auth_handler=self.authHandler,
                        captcha_handler=self.captchaHandler)

        try:
            self.vk.auth(reauth=True)
        except Exception as ex:
            self.screenManagement.transition.direction = "left"
            self.screenManagement.current = "auth"

            print(ex)

            return

        self.audio = vkapi.audio(self.vk)
        self.tracksCount = self.audio.get_len_user_audio()

        if self.tracksCount != 0:
            self.startScreen.tracksCount.label = "Аудиозаписей: " + str(self.tracksCount)
        else:
            self.startScreen.tracksCount.label = "Нет аудиозаписей"

        user = self.vk.method("users.get", {"user_ids": self.audio.user_id, "fields": "photo_200"})

        self.startScreen.username.text = user[0]["first_name"] + ' ' + "Валов"
        self.startScreen.avatar.source = user[0]["photo_200"]

        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "start"

    def enterButtonPressed(self, instance):
        self.screenManagement.transition.direction = "left"
        self.screenManagement.current = "loading"

        initThread = threading.Thread(target=self.initializeTracksCount)
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
        self.resultScreen("Сто баксов", "Дикая деревня", (bool(randint(0, 1)), bool(randint(0, 1))))
        t = threading.Thread(target=self.wait_and_change)
        t.start()

    def wait_and_change(self):
        time.sleep(3)
        self.overScreen(randint(0, 360))
        self.screenManagement.current = "over"

    def startGamePressed(self, instance):
        GameSession(self)

    def backButtonPressed(self, instance):
        self.screenManagement.current = "start"

    def build(self):
        self.screenManagement = ScreenManager(transition=SlideTransition())

        Builder.load_string(screens.game_helper)

        self.gameScreen = screens.game()
        self.resultScreen = screens.result()
        self.overScreen = screens.over()

        self.gameScreen.init_binds(self.check_song)
        self.overScreen.back_btn.bind(on_press=self.backButtonPressed)

        self.authScreen = screens.auth(name="auth")
        self.twoFactorScreen = screens.two_factor(name="two_factor")
        self.captchaScreen = screens.captcha(name="captcha")
        self.loadingScreen = screens.loading(name="loading")
        self.startScreen = screens.start(name="start")
        self.aboutScreen = screens.about(name="about")

        self.twoFactorScreen.enterButton.bind(on_press=self.twoFactorButtonPressed)
        self.authScreen.enterButton.bind(on_press=self.enterButtonPressed)
        self.captchaScreen.enterButton.bind(on_press=self.captchaButtonPressed)
        self.startScreen.aboutGame.bind(on_press=self.aboutGamePressed)
        self.startScreen.exitFromAccount.bind(on_press=self.exitButtonPressed)
        self.startScreen.startToPlay.bind(on_press=self.startGamePressed)
        self.aboutScreen.backButton.bind(on_press=self.backFromAboutPressed)

        for one in (self.authScreen, self.twoFactorScreen, self.captchaScreen, self.loadingScreen,
                    self.startScreen, self.aboutScreen, self.gameScreen, self.resultScreen,
                    self.overScreen):
            self.screenManagement.add_widget(one)

        return self.screenManagement


class GameSession:
    audio_ready = threading.Event()

    def __init__(self, app: MainApp):
        self.score = 0
        self.listens_left = 2
        self.playback_sec = 30
        self.root = app
        self.audio = app.audio
        self.audios = None
        self.curr_audio = None
        self.audio_sound = None
        self.start_first_loading()

    def prepare_audio(self):
        if self.audios is None:
            self.audios = self.audio.get_ids()
        self.curr_audio = self.get_random_audio()
        self.root.gameScreen.slider.max = self.playback_sec
        self.root.screenManagement.current = 'game'

    @mainthread
    def start_first_loading(self):
        self.root.screenManagement.current = "loading"
        self.root.gameScreen.init_binds(self.end_round)
        t1 = threading.Thread(target=self.prepare_audio)
        t1.start()

    def get_random_audio(self):
        index = randint(0, len(self.audios))
        info = self.audio.get_audio_by_id(*self.audios[index])
        if info['duration'] > 300:
            del self.audios[index]
            return self.get_random_audio()
        start = randint(0, info['duration']-self.playback_sec)*1000
        try:
            _audio.download(info['url'], CACHE_PATH)
        except FileNotFoundError:
            os.mkdir(CACHE_PATH)
            _audio.download(info['url'], CACHE_PATH)
        _audio.execute_segment(start, start+self.playback_sec*1000, CACHE_PATH)
        self.audio_sound = SoundLoader.load("short.mp3")

        print("WoW")
        return info

    def play(self):
        self.root.gameScreen.play_btn.disabled = True
        self.root.gameScreen.stop_btn.disabled = False
        self.t1 = threading.Thread(target=self.move_slider)
        self.t2 = threading.Thread(target=self.audio_sound.play)
        self.t1.start()
        self.t2.start()

    def move_slider(self):
        while self.audio_sound.state == 'play':
            self.root.gameScreen.slider.value = self.audio_sound.get_pos()
            time.sleep(0.5)
        self.root.gameScreen.slider.value = 0
        self.root.gameScreen.play_btn.disabled = False
        self.root.gameScreen.stop_btn.disabled = True

    def start_round(self):
        pass

    def end_round(self, instance):
        pass


if __name__ == "__main__":
    MainApp().run()
