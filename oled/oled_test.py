import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# I2C
i2c = busio.I2C(board.SCL, board.SDA)

# OLED (address 0x3C)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Clear
oled.fill(0)
oled.show()

# Create image
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

draw.text((0, 0), "OLED OK", font=font, fill=255)
draw.text((0, 15), "I2C: 0x3C", font=font, fill=255)
draw.text((0, 30), "Hackathon Ready", font=font, fill=255)

oled.image(image)
oled.show()
