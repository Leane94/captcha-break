from PIL import Image
import os
from img_process import rotate_and_cut, clearNoise
import random
import math
from utils import str2vec
import numpy as np


def load_templates():
    """ load the letter template from ./templates """
    templates = []
    list = os.listdir("./templates")
    for i in range(0, len(list)):
        image_path = os.path.join(".", "templates", list[i])
        templates.append((list[i].split(".")[0], Image.open(image_path).convert("L")))
    return templates


def create_captcha(templates):

    captcha = Image.new('RGBA', (200, 50), (255, 255, 255, 0))
    captcha_str = ""
    for i in range(4):
        number = random.randint(0, len(templates)-1)
        captcha_str += str(templates[number][0])
        template = templates[number][1]
        template = rotate_and_cut(template, random.randint(-45, 45))
        width_range = math.fabs(40 - template.size[0])
        height_range = math.fabs(50 - template.size[1])

        start_x_pos = i * 45 + random.randint(-width_range-5, width_range+5)
        start_y_pos = random.randint(0, height_range)

        captcha.paste(template, (start_x_pos, start_y_pos), mask=template)
    return captcha, captcha_str


def gen_dataset(num, templates):
    # print("generating %d dataset..." % num)
    dataset = []
    labels = []
    for _ in range(num):
        captcha, captcha_str = create_captcha(templates)
        dataset.append(np.asarray(captcha.convert("L")).reshape([50 * 200]) / 255)
        labels.append(str2vec(captcha_str))

    return np.array(dataset), np.array(labels)
