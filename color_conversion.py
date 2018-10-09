# This script contains function to convert RGB values to L*a*b values
# The goal is to calculate the human-perceived distance between colors
# For this we use the deltaE formula (euclidean distance in Lab color space)
import numpy as np


def rgb_to_lab(rgb):
    # this conversion is taken from https://gist.github.com/manojpandey/f5ece715132c572c80421febebaf66ae
    r = float(rgb[0]) / 255
    g = float(rgb[1]) / 255
    b = float(rgb[2]) / 255

    num = 0
    RGB = [0, 0, 0]
    for value in [r, g, b]:
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value /= 12.92

        RGB[num] = value * 100
        num += 1

    XYZ = [0, 0, 0]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    # Observer= 2°, Illuminant= D65
    XYZ[0] = float(XYZ[0]) / 95.047  # ref_X =  95.047
    XYZ[1] = float(XYZ[1]) / 100.0  # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883  # ref_Z = 108.883

    num = 0
    for value in XYZ:
        if value > 0.008856:
            value = value ** (float(1 / 3))
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return Lab


def lab_to_rgb(lab):
    # use skimage package for transformation from lab to rgb
    from skimage import color

    lab_as_array = np.array(lab)
    lab_as_array = lab_as_array.reshape((1, 1, 3))
    rgb = color.lab2rgb(lab_as_array)

    return np.squeeze(rgb * 255)


def deltaE(rgb1, rgb2):
    import math
    # convert rgb values to lab space
    lab1 = rgb_to_lab(rgb1)
    lab2 = rgb_to_lab(rgb2)

    sum = 0
    for l1, l2 in zip(lab1, lab2):
        sum += (l1 - l2) ** 2

    return math.sqrt(sum)


d1 = deltaE([255, 123, 12], [255, 123, 155])
d2 = deltaE([255, 123, 12], [255, 99, 61])

lab_test = rgb_to_lab([100, 100, 100])
rgb_test = lab_to_rgb(lab_test)

# Expected that d2 is smaller than d1
print('d1: {}, d2: {}'.format(d1, d2))
# Should yield more or less [100, 100, 100]
print(rgb_test.round().astype(np.uint8))
