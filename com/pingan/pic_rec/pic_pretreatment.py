# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import glob
import re
from PIL import Image
import pytesseract
import logging
import aircv as ac


logging.basicConfig(level=1,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: '
                                   '%(message)s')

#单张图片增加对比度和亮度
def addWeight(img, alpha = 1.3, gamma = 10):
    mask = np.zeros(img.shape, dtype=np.uint8)
    alpha = alpha
    beta = 1 - alpha
    gamma = gamma
    img_dst = cv2.addWeighted(img, alpha, mask, beta, gamma)
    return img_dst

#批量图片增加对比度和亮度
def addWeights(src_path, tgt_path, suffix):
    if not os.path.exists(src_path):
        logging.error('The path [%s] is not exist' %src_path)
    if not os.path.exists(tgt_path):
        logging.error('The path [%s] is not exist' %tgt_path)
    pic_files = glob.glob(os.path.join(src_path, suffix))
    total = len(pic_files)
    counter = 1
    for pic_file in pic_files:
        logging.log(1, "Total of %d/%d" %(counter, total))
        img = cv2.imread(pic_file)
        img_dst = addWeight(img)
        img_dst_file = tgt_path + r'/' + os.path.basename(pic_file)
        cv2.imwrite(img_dst_file, img_dst)
        counter += 1

#获取证件编码
def getCode(text):
    if text is None:
        return None
    # 去掉text中的引号
    text = text.replace('\'', '@@@')
    text = text.replace('\"', '@@@')
    # 去掉空格
    text = text.replace(' ', '')
    # print(text)
    # 匹配统一社会信用代码
    code = re.findall(r'[0-9][0-9]44030[0-9A-Z]{11}', text.upper())
    # a匹配食品经营许可证号
    if len(code) < 1:
        code = re.findall(r'JY[0-9]44030[0-9]{8}', text.upper())
    # 匹配餐饮服务许可证
    if len(code) < 1:
        code = re.findall(r'20[1-2][0-9]44030[0-9]{7}', text.upper())
    # 医配食品流通许可证
    if len(code) < 1:
        code = re.findall(r'SP44030[0-9][1-2][0-9]{9}', text.upper())
    # 匹配营业执照号 -注册号
    if len(code) < 1:
        code = re.findall(r'44030[0-9]{10}', text.upper())
    if len(code) > 0:
        code = code[0]
    else:
        code = None
    return code

#使用tesserect解析图片
def parsePics(src_path, suffix, tgt_path = None):
    if not os.path.exists(src_path):
        logging.error('The path [%s] is not exist' %src_path)
    pic_files = glob.glob(os.path.join(src_path, suffix))
    total = len(pic_files)
    counter = 1
    for pic_file in pic_files:
        img = Image.open(pic_file)
        text = pytesseract.image_to_string(img, lang='eng')
        code = getCode(text)
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        if code is not None:
            mid_path = '/01'
        else:
            mid_path = '/02'
        #照片/添加的文字/左上角坐标/字体/字体大小/颜色/字体粗细
        cv2.putText(img, code, (100,100), cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        if tgt_path is not None:
            logging.log(1, "Total of %d/%d" % (counter, total))
            img_dst_file = tgt_path + mid_path + r'/' + os.path.basename(pic_file)
            cv2.imwrite(img_dst_file, img)
            counter += 1


def picMatch(img, templ):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    templ_gray = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)
    h, w = templ_gray.shape[:2]
    res = cv2.matchTemplate(img, templ, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    print(templ.shape)
    print(img_gray.shape)
    print(top_left, bottom_right)
    cv2.rectangle(img, top_left, bottom_right, 0, 2)
    cv2.imwrite('./template/1.jpg', img)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def resize(img, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    h, w = img.shape[:2]
    if width is None and height:
        return img
    if width is None:
        width = height



if __name__ == '__main__':
    src_path = r'E:\work\pingan\05_code\pic_recognition\com\pingan\pic_rec\source'
    tgt_path = r'E:\work\pingan\05_code\pic_recognition\com\pingan\pic_rec\target'
    parse_path = r'E:\work\pingan\05_code\pic_recognition\com\pingan\pic_rec\parse'
    suffix = r'*.jpg'
    text = ''
    # addWeights(src_path, tgt_path, suffix)

    # print(getCode('JY24403000001343'))

    # parsePics(tgt_path, suffix, parse_path)

    img_file = r'./template/003_bak.jpg'
    templ_file = r'./template/template_06.jpg'
    queryImage = cv2.imread(img_file)
    trainImage = cv2.imread(templ_file)
    # img = cv2.circle(queryImage, (460, 120), 2, (0,0,255), 2)
    # img = cv2.circle(queryImage, (460+230, 120+230), 2, (0, 0, 255), 2)

    # img2 = queryImage[120:120+230, 460:460+230,:]
    #
    # cv2.imwrite('./template/template_03.jpg', img2)

    picMatch(queryImage, trainImage)
    # sift = cv2.SIF
    # kp1, des1 = sift.detectAndCompute(queryImage, None)
    # kp2, des2 = sift.detectAndCompute(trainImage, None)
    # FLANN_INDEX_KDTREE = 0
    # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    # search_params = dict(checks=50)  # or pass empty dictionary
    # flann = cv2.FlannBasedMatcher(index_params, search_params)
    # matches = flann.knnMatch(des1, des2, k=2)
    # # 找出相匹配的特征点
    # for m, n in matches:
    #     if m.distance < 0.75 * n.distance:
    #         x1 = kp1[m.queryIdx].pt[0]
    #         y1 = kp1[m.queryIdx].pt[1]
    #         x2 = kp2[m.trainIdx].pt[0]
    #         y2 = kp2[m.trainIdx].pt[1]
    #         print(x1,y1, x2,y2)

    # pos = ac.find_template(queryImage, trainImage)
    # print(pos)
    #
    # pt1 = pos['rectangle'][0]
    # pt2 = pos['rectangle'][3]
    # print(pt1, pt2)
    #
    # queryImage = cv2.rectangle(queryImage, pt1, pt2, 255, 2)
    # cv2.imwrite('./template/1.jpg', queryImage)
    # cv2.imshow('test', queryImage)




    cv2.waitKey(0)
    cv2.destroyAllWindows()