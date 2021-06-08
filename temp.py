import time
import busio
import board
import math
import adafruit_amg88xx
from scipy.interpolate import griddata
import numpy as np
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import


i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]

grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# First define some constants to allow easy resizing of shapes.
BORDER = 20
FONTSIZE = 24

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
#disp = ili9341.ILI9341(spi,rotation=90,  # 2.2", 2.4", 2.8", 3.2"
                      cs=cs_pin,dc=dc_pin,rst=reset_pin,baudrate=BAUDRATE,)
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
disp.image(image)

while True:
    
    pixels = amg.pixels
    '''
    i = 0
    j = 0
    for row in amg.pixels:
        j = 0
        for temp in row:
            red = 0
            green = 0
            blue = 0
            if amg.pixels[i][j] > 40:
                red = 255
                green = 0
                blue = 0
            elif amg.pixels[i][j] >=30 and amg.pixels[i][j] <= 40:
                red = 255
                green = abs((5-(amg.pixels[i][j] - 30)) * 255 / 10)
                blue = 0
            elif amg.pixels[i][j] >=25 and amg.pixels[i][j] < 30:
                red = abs((amg.pixels[i][j] - 25) * 255 / 5)
                green = 255
                blue = 0
            elif amg.pixels[i][j] >=20 and amg.pixels[i][j] < 25:
                red = 0
                green = 255
                blue = abs((5 - (amg.pixels[i][j] - 20)) * 255 / 5)
            elif amg.pixels[i][j] >=15 and amg.pixels[i][j] < 20:
                red = 0
                green = abs((amg.pixels[i][j] - 15) * 255 / 5)
                blue = 255
            draw.rectangle(((15+(i*16)), j*16, (15+(i*16))+16, (j*16)+16), fill=(int(blue), int(green), int(red)))
            
            j += 1
        i += 1
    '''
    #bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic")
    i = 0
    j = 0
    for row in pixels:
        j=0
        for temp in row:
            red = 0
            green = 0
            blue = 0
            if pixels[i][j] > 40:
                red = 255
                green = 0
                blue = 0
            elif pixels[i][j] >=30 and pixels[i][j] <= 40:
                red = 255
                green = abs((5-(pixels[i][j] - 30)) * 255 / 10)
                blue = 0
            elif pixels[i][j] >=25 and pixels[i][j] < 30:
                red = abs((amg.pixels[i][j] - 25) * 255 / 5)
                green = 255
                blue = 0
            elif pixels[i][j] >=20 and pixels[i][j] < 25:
                red = 0
                green = 255
                blue = abs((5 - (amg.pixels[i][j] - 20)) * 255 / 5)
            elif pixels[i][j] >=15 and pixels[i][j] < 20:
                red = 0
                green = abs((pixels[i][j] - 15) * 255 / 5)
                blue = 255
            draw.rectangle(((15+(i*16)), j*16, (15+(i*16))+16, (j*16)+16), fill=(int(blue), int(green), int(red)))
            j+=1
        i+=1
        print(["{0:.1f}".format(temp) for temp in row])
    disp.image(image)
    print("\n")
    
    #time.sleep(1)