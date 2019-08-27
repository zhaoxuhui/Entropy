# coding=utf-8
import cv2
import numpy as np
from collections import Counter
from multiprocessing import Pool


def calcIJ(img_patch):
    total_p = img_patch.shape[0] * img_patch.shape[1]
    if total_p % 2 != 0:
        tem = img_patch.flatten()
        center_p = tem[total_p / 2]
        mean_p = (sum(tem) - center_p) / (total_p - 1)
        return (center_p, mean_p)
    else:
        print "modify patch size"


def calcEntropy2d(img, win_w=3, win_h=3, threadNum=6):
    height = img.shape[0]
    width = img.shape[1]

    ext_x = win_w / 2
    ext_y = win_h / 2

    # 考虑滑动窗口大小，对原图进行扩边，扩展部分灰度为0
    ext_h_part = np.zeros([height, ext_x], img.dtype)
    tem_img = np.hstack((ext_h_part, img, ext_h_part))
    ext_v_part = np.zeros([ext_y, tem_img.shape[1]], img.dtype)
    final_img = np.vstack((ext_v_part, tem_img, ext_v_part))

    new_width = final_img.shape[1]
    new_height = final_img.shape[0]

    # 依次获取每个滑动窗口的内容，将其暂存在list中
    patches = []
    for i in range(ext_x, new_width - ext_x):
        for j in range(ext_y, new_height - ext_y):
            patch = final_img[j - ext_y:j + ext_y + 1, i - ext_x:i + ext_x + 1]
            patches.append(patch)

    # 并行计算每个滑动窗口对应的i、j
    pool = Pool(processes=threadNum)
    IJ = pool.map(calcIJ, patches)
    pool.close()
    pool.join()
    # 串行计算速度稍慢，可以考虑使用并行计算加速
    # for item in patchs:
    #     IJ.append(calcIJ(item))

    # 循环遍历统计各二元组个数
    Fij = Counter(IJ).items()
    # 推荐使用Counter方法，如果自己写for循环效率会低很多
    # Fij = []
    # IJ_set = set(IJ)
    # for item in IJ_set:
    #     Fij.append((item, IJ.count(item)))

    # 计算各二元组出现的概率
    Pij = []
    for item in Fij:
        Pij.append(item[1] * 1.0 / (new_height * new_width))

    # 计算每个概率所对应的二维熵
    H_tem = []
    for item in Pij:
        h_tem = -item * (np.log(item) / np.log(2))
        H_tem.append(h_tem)

    # 对所有二维熵求和
    H = sum(H_tem)
    return H


if __name__ == '__main__':
    img1 = cv2.imread("../imgs/img3.jpg", cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread("../imgs/img4.jpg", cv2.IMREAD_GRAYSCALE)
    H1 = calcEntropy2d(img1, 3, 3)
    H2 = calcEntropy2d(img2, 3, 3)
    print H1, H2
