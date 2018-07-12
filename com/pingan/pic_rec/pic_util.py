# -*- coding: utf-8 -*-

import cv2
import tkinter.messagebox as box
import glob
import os
import tkinter as tk
from tkinter import *
from com.pingan.pic_rec.pic_pretreatment import resize
import numpy as np
import tkinter.filedialog as fd
import sys

# sys.setdefaultencoding('utf-8')


def show(event,x,y,flags,param):
    global  pt1, pt2, img, template_file, template_img, draw_flag, show_flag
    if event == cv2.EVENT_LBUTTONDOWN:
        pt1 = (x, y)
        draw_flag = True
    elif event == cv2.EVENT_MOUSEMOVE and draw_flag == True:
        pt2 = (x, y)
        # img = cv2.imread(pics[counter - 1])
        # img = resize(img, 800)
        img = source_img.copy()
        img_msg = '(%dx%d)' % (pt2[0] - pt1[0], pt2[1] - pt1[1])
        img = cv2.rectangle(img, (pt1[0] - 2, pt1[1] - 2), (pt2[0] + 2, pt2[1] + 2), (0, 255, 0), 2)
        img = cv2.rectangle(img, (pt1[0] - 3, pt1[1] - 30), (pt1[0] + 120, pt1[1]), (0, 255, 0),-1)
        img = cv2.putText(img, img_msg, (pt1[0], pt1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        draw_flag = False
        pt2 = (x, y)
        img = source_img.copy()
        img = cv2.rectangle(img, (pt1[0] -2, pt1[1]-2), (pt2[0]+2, pt2[1]+2), (0, 255, 0), 2)
        img_msg = '(%dx%d)' %(pt2[0]-pt1[0], pt2[1]-pt1[1])
        img = cv2.rectangle(img, (pt1[0] - 3, pt1[1] - 30), (pt1[0] + 120, pt1[1]), (0, 255, 0), -1)
        img = cv2.putText(img, img_msg, (pt1[0], pt1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        template_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0], :]
    elif event == cv2.EVENT_RBUTTONDOWN and template_img is not None:
        cv2.imwrite(template_file, template_img)
        show_flag = False
        cv2.destroyAllWindows()

def nextPic(val):
    global counter, tgt_path, msg, total,img, draw_flag, show_flag,source_img
    counter += val
    show_flag = True
    if counter > total:
        counter -= val
        box.showinfo('系统提示', '没有更多图片')
    elif counter <=0:
        counter -= val
        box.showinfo('系统提示', '已经是第一张')
    else:
        msg = '图片数量：%d/%d' % (counter, total)
        lbl.config(text=msg)
        win_name = 'test' + str(counter)
        template_file = tgt_path + str(counter) + '.jpg'
        img = cv2.imread(pics[counter - 1].encode('gbk').decode())
        img = resize(img, 800)
        source_img = np.zeros(img.shape, np.uint8)
        source_img = img.copy()
        # ims_show = PhotoImage(file=pics[counter - 1])
        # cv = Canvas(t_frame3, bg='white', width=200, height=150)
        # cv.pack(side=LEFT)
        cv2.namedWindow(win_name)
        cv2.setMouseCallback(win_name, show)
        while show_flag:
            cv2.imshow(win_name, img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
            elif k == 27:
                break
        cv2.destroyAllWindows()

def getFilePath():
    global pic_path, pics,msg, total,var_pic_path
    pic_path = fd.askdirectory()
    var_pic_path.set(pic_path)
    pics = glob.glob(os.path.join(pic_path, suffix))
    total = len(pics)
    msg = '图片数量：%d/%d' % (counter, total)
    lbl.config(text=msg)

if __name__ == '__main__':
    pic_file = r'./template/004_bak.jpg'
    template_file = r'./template/template_06.jpg'
    pic_path = r'./source/'
    tgt_path = r'./target/'
    suffix = '*.jpg'
    pt1 = None
    pt2 = None
    draw_flag = False
    show_flag = True
    counter = 1
    calc = [-1, 0, 1]
    template_img = None
    source_img = None
    pics = glob.glob(os.path.join(pic_path, suffix))
    total = len(pics)
    msg = '图片数量：%d/%d' %(counter, total)


    win = tk.Tk()
    win.geometry('300x100')
    win.title('图片样本制作')
    win.resizable(width=False, height=False)

    t_frame0 = Frame(win)
    t_frame0.pack(side=TOP)
    lbl_img = tk.Label(t_frame0, text='图片路径：')
    lbl_img.pack(side=LEFT)
    var_pic_path = StringVar()
    entry_name = tk.Entry(t_frame0, textvariable= var_pic_path)
    entry_name.pack(side = LEFT)
    var_pic_path.set(pic_path)


    btn_file = tk.Button(t_frame0, text='选择文件夹', command = getFilePath)
    btn_file.pack(side=LEFT, padx=5)

    t_frame1 = Frame(win)
    t_frame1.pack(side = TOP)
    lbl = tk.Label(t_frame1)
    lbl.config(text = msg)
    lbl.pack(side = LEFT)

    t_frame2 = Frame(win)
    t_frame2.pack(side=TOP)
    btn = tk.Button(t_frame2, text='上一张', command = lambda val = calc[0]:nextPic(val))
    btn.pack(side = LEFT, padx=5)
    btn = tk.Button(t_frame2, text='当前张', command = lambda val = calc[1]:nextPic(val))
    btn.pack(side=LEFT, padx=5)
    btn = tk.Button(t_frame2, text='下一张', command = lambda val = calc[2]:nextPic(val))
    btn.pack(side=LEFT, padx=5)

    # t_frame3 = Frame(win)
    # t_frame3.pack(side=TOP)


    win.mainloop()






