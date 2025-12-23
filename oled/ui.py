class OLEDUI:
    def __init__(self, display):
        self.display = display

        self.state = {
            "camera": "WAITING",
            "quality": "---",
            "pc": "OFF",
            "robot": "IDLE"
        }

    def update(self, key, value):
        if key in self.state:
            self.state[key] = value
            self.draw()

    def draw(self):
        d = self.display.draw
        w = self.display.width
        f = self.display.font

        d.rectangle((0, 0, w, 64), outline=0, fill=0)

        d.text((0, 0), "HACKATHON SYSTEM", font=f, fill=255)
        d.text((0, 12), "--------------------", font=f, fill=255)

        d.text((0, 24), f"Camera  : {self.state['camera']}", font=f, fill=255)
        d.text((0, 34), f"Quality : {self.state['quality']}", font=f, fill=255)
        d.text((0, 44), f"PC Link : {self.state['pc']}", font=f, fill=255)
        d.text((0, 54), f"Robot   : {self.state['robot']}", font=f, fill=255)

        self.display.render()
