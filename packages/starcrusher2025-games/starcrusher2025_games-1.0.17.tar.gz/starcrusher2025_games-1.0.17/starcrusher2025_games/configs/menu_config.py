class MenuConfig:
    def __init__(self, title="Game Menu", bgc=(0, 0, 0), bg_image_path=None):
        self.title = title
        self.bgc = bgc
        self.bg_image_path = bg_image_path

    def set_title(self, title):
        self.title = title

    def set_background_color(self, bgc):
        self.bgc = bgc

    def set_bg_image(self, image_path):
        self.bg_image_path = image_path
