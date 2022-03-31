import matplotlib as mp
import numpy as np
import cv2 as cv
from PIL import ImageFont, ImageDraw, Image

SPACE_BETWEEN_LINES = 326
LINE_OFFSET_LEFT = 8

LINE_COLOR = (131, 128, 126)

TEXT_TOP_OFFSET = 30
TEMP_TOP_OFFSET = 50
ICON_TOP_OFFSET = 100

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


def overlay_image(large_image, small_image, x_offset, y_offset):
    y1, y2 = y_offset, y_offset + small_image.shape[0]
    x1, x2 = x_offset, x_offset + small_image.shape[1]

    alpha_small = small_image[:, :, 3] / 255.0
    alpha_large = 1.0 - alpha_small

    for c in range(0, 3):
        large_image[y1:y2, x1:x2, c] = (alpha_small * small_image[:, :, c] + alpha_large * large_image[y1:y2, x1:x2, c])


def icon_file_lookup(icon_number):
    if icon_number == 1 or icon_number == 2 or icon_number == 4 or icon_number == 30:
        return "./icons/1,2,4,30.png"
    if icon_number == 3 or icon_number == 6 or icon_number == 20:
        return "./icons/3,6,20.png"
    if icon_number == 5:
        return "./icons/5.png"
    if icon_number == 7 or icon_number == 8 or icon_number == 19 or icon_number == 38:
        return "./icons/7,8,19,38.png"
    if icon_number == 11:
        return "./icons/11.png"
    if icon_number == 12 or icon_number == 18:
        return "./icons/12,18.png"
    if icon_number == 13 or icon_number == 14:
        return "./icons/13,14.png"
    if icon_number == 15 or icon_number == 16 or icon_number == 17:
        return "./icons/15,16,17.png"
    if icon_number == 21:
        return "./icons/21.png"
    if icon_number == 22 or icon_number == 23 or icon_number == 24 or icon_number == 25\
            or icon_number == 26 or icon_number == 29 or icon_number == 31:
        return "./icons/22,23,24,25,26,29,31.png"
    if icon_number == 32:
        return "./icons/32.png"
    if icon_number == 33 or icon_number == 34:
        return "./icons/33,34.png"
    if icon_number == 35:
        return "./icons/35.png"
    if icon_number == 36:
        return "./icons/36.png"
    if icon_number == 37:
        return "./icons/37.png"
    if icon_number == 39 or icon_number == 40:
        return "./icons/39,40.png"
    if icon_number == 41 or icon_number == 42:
        return "./icons/41,42.png"
    if icon_number == 43:
        return "./icons/43.png"
    if icon_number == 44:
        return "./icons/43.png"


def draw_icons():
    icons = [1, 3, 7, 12, 35, 41]

    lines = create_lines()[:-1]
    lines += lines

    for (line_x, icon) in zip(lines, icons):
        icon_image = cv.imread(icon_file_lookup(icon), -1)

        resized_icon_image = cv.resize(icon_image, (SPACE_BETWEEN_LINES - 140, SPACE_BETWEEN_LINES - 140), interpolation=cv.INTER_AREA)

        if icons.index(icon) < 3:
            overlay_image(image, resized_icon_image, line_x, ICON_TOP_OFFSET)
        else:
            overlay_image(image, resized_icon_image, line_x, ICON_TOP_OFFSET + HOUR_VERT_OFFSET)


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
draw_icons()

cv.imshow('image', image)
cv.waitKey(0)

cv.imwrite("./image.png", image)