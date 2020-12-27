from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)

        self.loadingGif = Image(source = "assets/loading.gif")
        self.loadingGif.size_hint = [0.25, 0.25]
        self.loadingGif.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.loadingGif.anim_delay = 0.06

        self.add_widget(self.loadingGif)