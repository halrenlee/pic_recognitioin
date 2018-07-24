# -*- coding: utf-8 -*-

import cv2
import glob
import os
import numpy as np

def imgCrop(img):
    h, w = img.shape[:2]

    left = int(w//2)
    rigth = int(w)
    top = int(h//6)
    bottom = int(3*h//5)
    tgt_img = img[top: bottom, left: rigth]
    return tgt_img



if __name__ == '__main__':
    # src_path = r'E:\work\pingan_tmp\pic美团\01_食品经营许可证1'
    # tgt_path = r'E:\work\pingan_tmp\pic美团\01_食品经营许可证1_1'
    src_path = r'E:\work\pingan_tmp\pic美团\01_食品经营许可证2'
    tgt_path = r'E:\work\pingan_tmp\pic美团\01_食品经营许可证2_2'

    suffix = '*.jpg'

    files = glob.glob(os.path.join(src_path, suffix))
    total = len(files)
    counter = 1

    for file in files:
        print('total of %d/%d' %(counter, total))
        print(file)
        # img = cv2.imread(file)
        img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), -1)
        tgt_img = imgCrop(img)
        tgt_img_name = tgt_path + '/' + os.path.basename(file)
        # cv2.imwrite(tgt_img_name, tgt_img)
        cv2.imencode('.jpg',tgt_img)[1].tofile(tgt_img_name)
        counter += 1


    #
    # img = cv2.imread(pic_file)
    # tgt_img = imgCrop(img)
