import shutil
import sys
import os
import time
#import progressbar
from time import sleep
from console_progressbar import ProgressBar
import threading
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import RPi.GPIO as  GPIO


def progress_percentage(perc, width=None):
    FULL_BLOCK = '>'
    INCOMPLETE_BLOCK_GRAD = ['x', '+', 'x',]

    assert(isinstance(perc, float))
    assert(0. <= perc <= 100.)

    if width is None:
        width = os.get_terminal_size().columns

    max_perc_widget = '[100.00%]' # 100% is max
    separator = ' '
    blocks_widget_width = width - len(separator) - len(max_perc_widget)
    assert(blocks_widget_width >= 10)
    perc_per_block = 100.0/blocks_widget_width
    epsilon = 1e-6
    full_blocks = int((perc + epsilon)/perc_per_block)

    empty_blocks = blocks_widget_width - full_blocks

    blocks_widget = ([FULL_BLOCK] * full_blocks)
    blocks_widget.extend([INCOMPLETE_BLOCK_GRAD[0]] * empty_blocks)
    remainder = perc - full_blocks*perc_per_block

    if remainder > epsilon:
        grad_index = int((len(INCOMPLETE_BLOCK_GRAD) * remainder)/perc_per_block)
        blocks_widget[full_blocks] = INCOMPLETE_BLOCK_GRAD[grad_index]

    str_perc = '%.2f' % perc
    perc_widget = '[%s%%]' % str_perc.ljust(len(max_perc_widget) - 3)
    progress_bar = '%s%s%s' % (''.join(blocks_widget), separator, perc_widget)
    return ''.join(progress_bar)


def copy_progress(copied, total):
    print('\r' + progress_percentage(100*copied/total, width=25), end='')
    per=100*copied/total
    led.draw_text2(52, 10, per, 1)
    led.display()

def copyfile(src, dst, *, follow_symlinks=True):
    if shutil._samefile(src, dst):
        raise shutil.SameFileError("{!r} and {!r} are the same file".format(src, dst))

    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:

            pass
        else:

            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError("`%s` is a named pipe" % fn)

    if not follow_symlinks and os.path.islink(src):
        os.symlink(os.readlink(src), dst)
    else:
        size = os.stat(src).st_size
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                copyfileobj(fsrc, fdst, callback=copy_progress, total=size)
    return dst


def copyfileobj(fsrc, fdst, callback, total, length=16*1024):
    copied = 0
    while True:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
        copied += len(buf)
        callback(copied, total=total)


def copy_with_progress(src, dst, *, follow_symlinks=True):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst, follow_symlinks=follow_symlinks)
    shutil.copymode(src, dst)
    return dst


def copydir(src, dst):
    print(src)
    bar = progressbar.ProgressBar(maxval=20, \
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    if os.path.isfile(src)==True:
        start=time.time()
        bar.start()
        print("SENDING..")
        bar.update(shutil.copy(src, dst))
        end=time.time()
        bar.finish()
        print("TOTAL TIME",end-start)

    elif os.path.isdir(src)==True:
        ssrc=os.listdir(src)
        h=0
        for names in ssrc:
            if os.path.isdir(ssrc[h])==True:
                start=time.time()
                bar.start()
                path_ssrc=str(src)+"/"+str(ssrc[int(h)])
                print("SENDING..")
                bar.update(shutil.copytree(path_ssrc, dst))
                end=time.time()
                bar.finish()
                print("TOTAL TIME",end-start)
                h=h+1
            else:
                path_ssrc_f=str(src)+"/"+str(ssrc[int(h)])
                print("SENDING..")
                copydir(path_ssrc_f, dst)
                h=h+1


path = ('E:/')
files=os.listdir(path)
siz1=len(files)
nu=0
print('SELECT THE RECIVER AND THE SENDER\n')
for name in files:
    print('FOR',name,'PRESS',nu)
    nu=nu+1

rinpt = input('RECIVER:\n')

sinpt = input('SENDER:\n')
if rinpt== 'q' or sinpt=='q':
    quit()
spath_name="E:/"+str((files[int(sinpt)]))
spath=(spath_name)
lst_spath=os.listdir(spath)
siz_spath=len(lst_spath)
if siz_spath == 0:
    print("NO FILES TO SEND\nQUITING...")
    time.sleep(3)
    quit()
while True:
    y=0
    for names in lst_spath:
        print('FOR',names,'PRESS',y)
        y=y+1

    choice= input('ENTER UR CHOICE: ')
    if choice == 'q':
        quit()
    else:
        nsrc = "E:/"+str((files[int(sinpt)]))+"/"+str((lst_spath[int(choice)]))
        ndes = "E:/"+str((files[int(rinpt)]))
        print(nsrc)
        print(ndes)
        copy_with_progress(nsrc,ndes)









