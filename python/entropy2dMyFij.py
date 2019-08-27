# coding=utf-8
import cv2
import numpy as np
import time
from numba import jit


@jit(nopython=True)
def calcFij(tup_list):
    tup_list.sort()

    times = []
    times.append(0)
    for i in range(len(tup_list) - 1):
        if tup_list[i] == tup_list[i + 1]:
            times.append(1)
        else:
            times.append(0)

    times2 = []
    sum = 0
    for i in range(len(times) - 1):
        # 0-0 1-0
        if times[i] == 0 and times[i + 1] == 0:
            times2.append(times[i] + 1)
        elif times[i] == 1 and times[i + 1] == 0:
            times2.append(sum + 1)
            sum = 0
        # 0-1 1-1
        else:
            sum += 1
            if i == len(times) - 2:
                times2.append(sum + 1)
    if times[-1] == 0:
        times2.append(1)
    return times2


@jit(nopython=True)
def calcIJ(img_patch):
    total_p = img_patch.shape[0] * img_patch.shape[1]
    if total_p % 2 != 0:
        center_p = img_patch[img_patch.shape[0] / 2, img_patch.shape[1] / 2]
        mean_p = (np.sum(img_patch) - center_p) / (total_p - 1)
        return (center_p, mean_p)
    else:
        pass


def calcEntropy2dSpeedUp(img, win_w=3, win_h=3):
    height = img.shape[0]

    ext_x = win_w / 2
    ext_y = win_h / 2

    ext_h_part = np.zeros([height, ext_x], img.dtype)
    tem_img = np.hstack((ext_h_part, img, ext_h_part))
    ext_v_part = np.zeros([ext_y, tem_img.shape[1]], img.dtype)
    final_img = np.vstack((ext_v_part, tem_img, ext_v_part))

    new_width = final_img.shape[1]
    new_height = final_img.shape[0]

    t1 = time.time()
    # 最耗时的步骤，遍历计算二元组
    IJ = []
    for i in range(ext_x, new_width - ext_x):
        for j in range(ext_y, new_height - ext_y):
            patch = final_img[j - ext_y:j + ext_y + 1, i - ext_x:i + ext_x + 1]
            ij = calcIJ(patch)
            IJ.append(ij)
    t2 = time.time()
    print 'calc IJ time', t2 - t1

    print 'start calculating...'
    t3 = time.time()
    Fij = calcFij(IJ)
    t4 = time.time()
    print 'IJ len', len(IJ), 'Fij len', len(Fij)
    print 'fij time', t4 - t3

    t5 = time.time()
    # 第二耗时的步骤，计算各二元组出现的概率
    Pij = []
    for item in Fij:
        tmp_p = item * 1.0 / (new_height * new_width)
        Pij.append(tmp_p)
    t6 = time.time()
    print 'pij time', t6 - t5

    t7 = time.time()
    H_tem = []
    for item in Pij:
        h_tem = -item * (np.log(item) / np.log(2))
        H_tem.append(h_tem)

    H = np.sum(H_tem)
    t8 = time.time()
    print 'h tem time', t8 - t7
    return H


if __name__ == '__main__':
    img1 = cv2.imread("../imgs/img11.jpg", cv2.IMREAD_GRAYSCALE)
    t1 = time.time()
    H1 = calcEntropy2dSpeedUp(img1, 3, 3)
    t2 = time.time()
    print "\n"
    print 'all time', t2 - t1
    print 'H', H1
