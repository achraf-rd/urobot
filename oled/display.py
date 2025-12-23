import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont


class OLEDDisplay:
    def __init__(self, width=128, height=64):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(width, height, self.i2c)

        self.width = width
        self.height = height

        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()

        self.clear()

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.oled.fill(0)
        self.oled.show()

    def render(self):
        self.oled.image(self.image)
        self.oled.show()
