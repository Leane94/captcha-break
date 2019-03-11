from PIL import Image, ImageDraw
import numpy as np


def rotate(img, angle):
    """ rotate the image """
    im2 = img.convert('RGBA')
    rot = im2.rotate(angle, expand=1)
    fff = Image.new('RGBA', rot.size, (255,) * 4)
    out = Image.composite(rot, fff, rot)
    return out.convert(img.mode)


def cut(img):
    """ cut the redundant white padding of the image """
    img_arr = np.asarray(img)
    row = [0, 0]  # the cut row range
    col = [0, 0]  # the cut column range
    # search for row
    for y in range(img_arr.shape[1]):
        count = 0
        for x in range(img_arr.shape[0]):
            if img_arr[y, x] == 255:
                count += 1

        if count != img_arr.shape[0]:
            if row[0] == 0:
                row[0] = y-1
            else:
                row[1] = y+1

    # search for column
    for x in range(img_arr.shape[0]):
        count = 0
        for y in range(img_arr.shape[1]):
            if img_arr[y, x] == 255:
                count += 1
        if count != img_arr.shape[1]:
            if col[0] == 0:
                col[0] = x-1
            else:
                col[1] = x+1

    return Image.fromarray(np.uint8(img_arr[row[0]: row[1], col[0]: col[1]]))


def getPixel(image, x, y):
    L = image.getpixel((x, y))
    if L == 0:
        nearDots = 0
        if inRange(image, x - 1, y - 1) and L - image.getpixel((x - 1, y - 1)):
            nearDots += 1
        if inRange(image, x - 1, y) and L - image.getpixel((x - 1, y)):
            nearDots += 1
        if inRange(image, x - 1, y + 1) and L - image.getpixel((x - 1, y + 1)):
            nearDots += 1
        if inRange(image, x, y - 1) and L - image.getpixel((x, y - 1)):
            nearDots += 1
        if inRange(image, x, y + 1) and L - image.getpixel((x, y + 1)):
            nearDots += 1
        if inRange(image, x + 1, y - 1) and L - image.getpixel((x + 1, y - 1)):
            nearDots += 1
        if inRange(image, x + 1, y) and L - image.getpixel((x + 1, y)):
            nearDots += 1
        if inRange(image, x + 1, y + 1) and L - image.getpixel((x + 1, y + 1)):
            nearDots += 1
        if nearDots >= 7:
            return 1
        elif nearDots == 6:
            nearDots = 0
            if inRange(image, x - 2, y - 2) and L - image.getpixel((x - 2, y - 2)):
                nearDots += 1
            if inRange(image, x - 2, y) and L - image.getpixel((x - 2, y)):
                nearDots += 1
            if inRange(image, x - 2, y + 2) and L - image.getpixel((x - 2, y + 2)):
                nearDots += 1
            if inRange(image, x, y - 2) and L - image.getpixel((x, y - 2)):
                nearDots += 1
            if inRange(image, x, y + 2) and L - image.getpixel((x, y + 2)):
                nearDots += 1
            if inRange(image, x + 2, y - 2) and L - image.getpixel((x + 2, y - 2)):
                nearDots += 1
            if inRange(image, x + 2, y) and L - image.getpixel((x + 2, y)):
                nearDots += 1
            if inRange(image, x + 2, y + 2) and L - image.getpixel((x + 2, y + 2)):
                nearDots += 1
            if nearDots >= 7:
                return 1
            else:
                return 0
    else:
        return 1


def inRange(image, x, y):
    if x >= image.size[0] or y >= image.size[1]:
        return False
    else:
        return True


def clearNoise(image):
    draw = ImageDraw.Draw(image)
    for x in range(0, image.size[0]):
        for y in range(0, image.size[1]):
            color = getPixel(image, x, y)
            draw.point((x, y), color)


def rotate_and_cut(im, degree):
    im = rotate(im, degree)
    im = cut(im)
    im.convert("L")
    im = im.point(lambda x: 0 if x < 130 else x >= 130, '1')
    clearNoise(im)
    im = im.convert("RGBA")
    datas = im.getdata()
    newData = list()
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append((0, 0, 0, 255))

    im.putdata(newData)
    return im

