# -*- coding: utf-8 -*-
import base64
import os
import random
import time
import shutil
import stat
import Tkinter, tkFileDialog
from icon import img

USB = 'F:'  # u盘目录,初始设置F：盘用于测试
SAVE = 'C:/usbCopy'  # 保存目录，默认为C:/usbCopy
OLD = []  # 保存文件目录，用于判断U盘文件用没有变化
dict = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0,
        'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}


# U盘拷贝
def usbWalker():
    global SAVE
    global USB
    if os.path.exists(SAVE):
        print 'DELETE EXIST FILE !'
        try:
            os.chmod(SAVE, stat.S_IREAD | stat.S_IWRITE)
            shutil.rmtree(SAVE)
        except Exception, e:
            print e
            SAVE = SAVE + 'NewFile' + str(random.random() * 10)

    print 'FileName  ' + SAVE
    print 'Copy...'

    USB = USB.decode('gbk')
    SAVE = SAVE.decode('gbk')
    shutil.copytree(USB, SAVE)  # 人生苦短，我用python


# 判断U盘内容是否变化
def getUsb():
    global OLD
    NEW = os.listdir(USB)
    if (len(NEW) == len(OLD)):
        print "U盘内容没有变化"
        return 0
    else:
        OLD = NEW
        return 1


# 判断U盘是否存在
def usbCopy():
    global USB
    for i in range(26):
        name = chr(i + ord('A')) + ':'
        print name
        if os.path.exists(name):
            dict[chr(i + ord('A'))] = 1
            print '存在磁盘' + chr(i + ord('A'))

    while (1):
        for i in range(26):
            name = chr(i + ord('A')) + ':'
            if not os.path.exists(name):
                dict[chr(i + ord('A'))] = 0
            if os.path.exists(name) and dict[chr(i + ord('A'))] == 0:
                USB = name
                print "检测到U盘"
                if getUsb():
                    try:
                        usbWalker()
                    except Exception, e:
                        print Exception, e

        print "暂时没有U盘,开始休眠"
        time.sleep(1)  # 休眠时间
        print "休眠结束"


def choseDir():
    global SAVE
    SAVE = tkFileDialog.askdirectory(parent=root, initialdir="/", title='Pick a directory') + '/usbCopy'
    print 'SAVE IN ' + SAVE


def clickButton():
    root.withdraw()
    usbCopy()


if __name__ == '__main__':
    root = Tkinter.Tk()
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    root.iconbitmap("tmp.ico")
    root.title('USB Dumper')
    root.geometry('700x400')
    Tkinter.Label(root,
                  text='\n\nYou can use this application to automatically copy \nthe files and folders from the USB '
                       'that is connected to your computer\n Default file path:   C:\usbCopy\n\nSolemnly swear that you are up to no good\n').pack()
    Tkinter.Label(root, text=' Bug report:\ngithub.com/Ginray/USB-Dumper/issues\n\n').pack()
    Tkinter.Button(root, text='Change Save Directory', command=choseDir).pack()
    Tkinter.Button(root, text='Start USB Dumper', command=clickButton).pack()
    root.mainloop()
