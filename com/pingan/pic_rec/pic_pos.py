# -*- coding: utf-8 -*-

import cv2
import tkinter.messagebox as box


def show(event,x,y,flags,param):
    global  pt1, pt2, img, template_file
    if event == cv2.EVENT_LBUTTONDOWN:
        if pt1 is None:
            pt1 = (x, y)
        elif pt2 is None:
            pt2 = (x, y)
    if pt1 is not None and pt2 is not None:
        template_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0],:]
        cv2.imwrite(template_file, template_img)
        pt1 = None
        pt2 = None
        box.showinfo('msg', 'get ok')

if __name__ == '__main__':
    pic_file = r'./template/004_bak.jpg'
    template_file = r'./template/template_06.jpg'


    pt1 = None
    pt2 = None

    img = cv2.imread(pic_file)
    cv2.imshow('test', img)
    cv2.setMouseCallback('test', show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()