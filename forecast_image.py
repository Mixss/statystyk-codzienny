import matplotlib as mp
import numpy as np
import cv2 as cv
from PIL import ImageFont, ImageDraw, Image

SPACE_BETWEEN_LINES = 326
LINE_OFFSET_LEFT = 8

LINE_COLOR = (131, 128, 126)

TEXT_TOP_OFFSET = 30
TEMP_TOP_OFFSET = 50

HOUR_VERT_OFFSET = 400

# get dictionary
# hour: , temperature, icon(description), wind speed, wind dir
def create_lines():
    vertical_lines = []

    for i in range(4):
        vertical_lines.append(LINE_OFFSET_LEFT + i * SPACE_BETWEEN_LINES + i)

    return vertical_lines


def draw_lines():
    vertical_lines = create_lines()

    for x_coord in vertical_lines:
        cv.line(image, (x_coord, 5), (x_coord, image_height - 5), LINE_COLOR, 1)


def draw_temperatures(img, color, text_scale):
    temperatures = [3, 7, 18, 9, -3, 21]

    font = cv.FONT_HERSHEY_DUPLEX

    lines = create_lines()[:-1]

    lines += lines

    image_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(image_pil)

    for line_x, temp in zip(lines, temperatures):
        text_size = cv.getTextSize(str(temp), font, text_scale, 2)[0]

        center_x = line_x + SPACE_BETWEEN_LINES / 2

        unicode_font = ImageFont.truetype("./fonts/IBMPlexSansArabic-Light.ttf", 60)

        text_x = center_x - unicode_font.getsize(str(temp) + "°C")[0] / 2

        if temperatures.index(temp) < 3:
            draw.text((int(text_x), TEMP_TOP_OFFSET), str(temp) + "°C", font=unicode_font, fill=color)
            #cv.putText(image, str(temp) + "°C", (int(text_x), TEMP_TOP_OFFSET), font, text_scale, color, 1, bottomLeftOrigin=False, lineType=cv.LINE_AA)
        else:
            draw.text((int(text_x), TEMP_TOP_OFFSET + HOUR_VERT_OFFSET), str(temp) + "°C", font=unicode_font, fill=color)
            #cv.putText(image, str(temp) + "°C", (int(text_x), TEMP_TOP_OFFSET + HOUR_VERT_OFFSET), font, text_scale, color, 1, bottomLeftOrigin=False, lineType=cv.LINE_AA)

    return np.array(image_pil)


def draw_icons():
    

def draw_text(color, text_scale):
    hours = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]

    font = cv.FONT_HERSHEY_DUPLEX

    lines = create_lines()[:-1]

    lines += lines

    for line_x, hour in zip(lines, hours):
        # center text
        text_size = cv.getTextSize(hour, font, text_scale, 2)[0]

        center_x = line_x + SPACE_BETWEEN_LINES / 2

        text_x = center_x - text_size[0] / 2

        if hours.index(hour) < 3:
            cv.putText(image, hour, (int(text_x), TEXT_TOP_OFFSET), font, text_scale, color, 1, bottomLeftOrigin=False, lineType=cv.LINE_AA)
        else:
            cv.putText(image, hour, (int(text_x), TEXT_TOP_OFFSET + HOUR_VERT_OFFSET), font, text_scale, color, 1, bottomLeftOrigin=False, lineType=cv.LINE_AA)


image_width = 1000
image_height = 800
channels = 3
# color = (59, 53, 50)  # discord darker color
color = (63, 57, 54)

image = np.full((image_height, image_width, channels), color, dtype=np.uint8)

draw_lines()
draw_text((191, 188, 186), 0.9)
image = draw_temperatures(image, (221, 218, 216), 1.2)

cv.imshow('image', image)
cv.waitKey(0)

cv.imwrite("./image.png", image)