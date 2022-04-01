import matplotlib as mp
import numpy as np
import cv2 as cv
from PIL import ImageFont, ImageDraw, Image
import math

SPACE_BETWEEN_LINES = 326
LINE_OFFSET_LEFT = 8

LINE_COLOR = (131, 128, 126)

TEXT_TOP_OFFSET = 40
TEMP_TOP_OFFSET = 50
ICON_TOP_OFFSET = 150

HOUR_VERT_OFFSET = 400

WIND_SPEED_LEFT_OFFSET = 20
WIND_SPEED_TOP_OFFSET = 340


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


def overlay_image(large_image, small_image, x_offset, y_offset):
    y1, y2 = y_offset, y_offset + small_image.shape[0]
    x1, x2 = x_offset, x_offset + small_image.shape[1]

    alpha_small = small_image[:, :, 3] / 255.0
    alpha_large = 1.0 - alpha_small

    for c in range(0, 3):
        large_image[y1:y2, x1:x2, c] = (alpha_small * small_image[:, :, c] + alpha_large * large_image[y1:y2, x1:x2, c])


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result


def rotation(image, angleInDegrees):
    h, w = image.shape[:2]
    img_c = (w / 2, h / 2)

    rot = cv.getRotationMatrix2D(img_c, angleInDegrees, 1)

    rad = math.radians(angleInDegrees)
    sin = math.sin(rad)
    cos = math.cos(rad)
    b_w = int((h * abs(sin)) + (w * abs(cos)))
    b_h = int((h * abs(cos)) + (w * abs(sin)))

    rot[0, 2] += ((b_w / 2) - img_c[0])
    rot[1, 2] += ((b_h / 2) - img_c[1])

    out_img = cv.warpAffine(image, rot, (b_w, b_h), flags=cv.INTER_LINEAR)
    return out_img


def draw_temperatures(img, color, font_size):
    temperatures = [3, 7, 18, 9, -3, 21]

    font = cv.FONT_HERSHEY_DUPLEX

    lines = create_lines()[:-1]

    lines += lines

    image_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(image_pil)

    for line_x, temp in zip(lines, temperatures):

        center_x = line_x + SPACE_BETWEEN_LINES / 2

        unicode_font = ImageFont.truetype("./fonts/IBMPlexSansArabic-Light.ttf", font_size)

        text_x = center_x - unicode_font.getsize(str(temp) + "°C")[0] / 2

        if temperatures.index(temp) < 3:
            draw.text((int(text_x), TEMP_TOP_OFFSET), str(temp) + "°C", font=unicode_font, fill=color)
            # cv.putText(image, str(temp) + "°C", (int(text_x), TEMP_TOP_OFFSET), font, text_scale, color, 1, bottomLeftOrigin=False, lineType=cv.LINE_AA)
        else:
            draw.text((int(text_x), TEMP_TOP_OFFSET + HOUR_VERT_OFFSET), str(temp) + "°C", font=unicode_font,
                      fill=color)
            # cv.putText(image, str(temp) + "°C", (int(text_x), TEMP_TOP_OFFSET + HOUR_VERT_OFFSET), font, text_scale, color, 1, bottomLeftOrigin=False, lineType=cv.LINE_AA)

    return np.array(image_pil)


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
    if icon_number == 22 or icon_number == 23 or icon_number == 24 or icon_number == 25 \
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

        resized_icon_image = cv.resize(icon_image, (SPACE_BETWEEN_LINES - 180, SPACE_BETWEEN_LINES - 180),
                                       interpolation=cv.INTER_AREA)

        center_x = line_x + SPACE_BETWEEN_LINES / 2

        icon_x = center_x - resized_icon_image.shape[0] / 2

        if icons.index(icon) < 3:
            overlay_image(image, resized_icon_image, int(icon_x), ICON_TOP_OFFSET)
        else:
            overlay_image(image, resized_icon_image, int(icon_x), ICON_TOP_OFFSET + HOUR_VERT_OFFSET)


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
            cv.putText(image, hour, (int(text_x), TEXT_TOP_OFFSET), font, text_scale, color, 1, bottomLeftOrigin=False,
                       lineType=cv.LINE_AA)
        else:
            cv.putText(image, hour, (int(text_x), TEXT_TOP_OFFSET + HOUR_VERT_OFFSET), font, text_scale, color, 1,
                       bottomLeftOrigin=False, lineType=cv.LINE_AA)


def draw_wind(color, text_scale):
    wind_directions = [0, 45, 90, 180, 243, 321]
    wind_speeds = [32.1, 54.1, 3.1, 0.1, 45.2, 20.3]

    lines = create_lines()[:-1]
    lines += lines

    font = cv.FONT_HERSHEY_DUPLEX

    arrow_image = cv.imread("./icons/arrow.png", -1)
    resized_arrow_image = cv.resize(arrow_image, (int(arrow_image.shape[0] * 0.5), int(arrow_image.shape[1] * 0.5)),
                                    interpolation=cv.INTER_AREA)

    for line_x, direction, speed in zip(lines, wind_directions, wind_speeds):
        text_size = cv.getTextSize(str(speed), font, text_scale, 2)[0]

        center_x = line_x + SPACE_BETWEEN_LINES / 2

        text_x = center_x - text_size[0] / 2

        rotated_arrow_image = rotation(resized_arrow_image, direction)

        if wind_speeds.index(speed) < 3:
            cv.putText(image, str(speed), (int(text_x) + WIND_SPEED_LEFT_OFFSET, WIND_SPEED_TOP_OFFSET), font,
                       text_scale, color, 1, bottomLeftOrigin=False, lineType=cv.LINE_AA)

            text_y = text_size[1] / 2 + WIND_SPEED_TOP_OFFSET

            overlay_image(image, rotated_arrow_image, int(text_x - 35), int(text_y - rotated_arrow_image.shape[1] / 2 - 20))
        else:
            cv.putText(image, str(speed), (int(text_x) + WIND_SPEED_LEFT_OFFSET, WIND_SPEED_TOP_OFFSET +
                                           HOUR_VERT_OFFSET), font, text_scale, color, 1, bottomLeftOrigin=False,
                       lineType=cv.LINE_AA)

            text_y = text_size[1] / 2 + WIND_SPEED_TOP_OFFSET + HOUR_VERT_OFFSET

            overlay_image(image, rotated_arrow_image, int(text_x - 35), int(text_y - rotated_arrow_image.shape[1] / 2 - 20))


image_width = 1000
image_height = 800
channels = 3
# color = (59, 53, 50)  # discord darker color
color = (63, 57, 54)

image = np.full((image_height, image_width, channels), color, dtype=np.uint8)

draw_lines()
draw_text((191, 188, 186), 1.0)
image = draw_temperatures(image, (221, 218, 216), 86)
draw_icons()
draw_wind((191, 188, 186), 1.3)

cv.imshow('image', image)
cv.waitKey(0)

cv.imwrite("./generated_images/image.png", image)
