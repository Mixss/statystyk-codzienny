import matplotlib as mp
import numpy as np
import cv2 as cv


# get dictionary
# hour: , temperature, icon(description), wind speed, wind dir
def create_lines():
    vertical_lines = []

    for i in range(7):
        vertical_lines.append(8 + i * 163 + i)

    return vertical_lines


def draw_lines():
    vertical_lines = create_lines();

    for x_coord in vertical_lines:
        cv.line(image, (x_coord, 5), (x_coord, image_height - 5), (131, 128, 126), 1)


def draw_text(color, text_scale):
    hours = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]

    font = cv.FONT_HERSHEY_DUPLEX

    lines = create_lines()

    for line_x, hour in zip(lines, hours):
        # center text
        text_size = cv.getTextSize(hour, font, text_scale, 2)[0]

        center_x = line_x + 163 / 2

        text_x = center_x - text_size[0] / 2

        cv.putText(image, hour, (int(text_x), 30), font, text_scale, color, 1, bottomLeftOrigin=False)



image_width = 1000
image_height = 250
channels = 3
# color = (59, 53, 50)  # discord darker color
color = (63, 57, 54)

image = np.full((image_height, image_width, channels), color, dtype=np.uint8)

draw_lines()
draw_text((191, 188, 186), 0.6)

cv.imshow('image', image)
cv.waitKey(0)

cv.imwrite("./image.jpg", image)
