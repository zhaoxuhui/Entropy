# coding=utf-8
import cv2
import numpy as np
import os.path as path


def calcEntropy(img):
    entropy = []

    hist = cv2.calcHist([img], [0], None, [256], [0, 255])
    total_pixel = img.shape[0] * img.shape[1]

    for item in hist:
        probability = item / total_pixel
        if probability == 0:
            en = 0
        else:
            en = -1 * probability * (np.log(probability) / np.log(2))
        entropy.append(en)

    arr = np.asarray(entropy, dtype="object")
    sum_en = np.sum(arr)
    return sum_en


if __name__ == '__main__':
    currentFilePath = path.dirname(path.realpath(__file__))
    img1 = cv2.imread(currentFilePath + "/../imgs/img1.jpg", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(currentFilePath + "/../imgs/img2.jpg", cv2.IMREAD_GRAYSCALE)

    entropy1 = calcEntropy(img1)
    entropy2 = calcEntropy(img2)

    print(entropy1)
    print(entropy2)
