import PIL
import numpy as np
import win32api, win32con, win32clipboard
import os
import time


def a(x=0, y=0):
    return np.array((x, y), dtype=np.int32)


# ------------------------
# ---  USER VARIABLES  ---
# --- UPDATE EVERY RUN ---
# TODO: Pull data from reports (write tmp, read info, rename, repeat)
year = 1965
last_game_number = 143
desktop_path = "\\\\CNOCMF01\\Staff_C$\\rwconner\\Desktop\\"
# desktop_path = "C:\\Users\\pants\\Desktop\\fantasybaseball\\"
# --- END USER VARIABLES ---
#
# --- DO NOT CHANGE ------
NUMBER_OF_REPORTS = 8
SLEEP = 0.3
# MAG = 1
MAG = 1.25
DESKTOP_SIZE = a(1920, 1080)
# ---  END  VARIABLES  ---
# ------------------------

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(SLEEP)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(SLEEP)
    print "mouse Left Click."  # completely optional. But nice for debugging purposes.


def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(SLEEP)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
    time.sleep(SLEEP)
    print "mouse Right Click."  # completely optional. But nice for debugging purposes.


def mousePos(coord=a(0, 0)):
    scaledPos = (coord / MAG).astype(int)
    print "mouse to ({0})".format(scaledPos)
    win32api.SetCursorPos(scaledPos)
    time.sleep(SLEEP)


def enter():
    print "Keystroke [Enter]"
    win32api.keybd_event(0xD, 0, 0, 0)  # Enter
    time.sleep(0.05)
    win32api.keybd_event(0xD, 0, 2, 0)  # Enter
    time.sleep(0.05)


def ctrlV():
    print "Keystroke [ctrl + V]"
    win32api.keybd_event(0x11, 0, 0, 0)  # Ctrl
    time.sleep(0.05)
    win32api.keybd_event(0x56, 0, 0, 0)  # V
    time.sleep(0.05)
    win32api.keybd_event(0x56, 0, 2, 0)  # V
    time.sleep(0.05)
    win32api.keybd_event(0x11, 0, 2, 0)  # Ctrl
    time.sleep(0.05)


def closeReport():
    """ctrl + F4"""
    print "Keystroke [ctrl + F4]"
    win32api.keybd_event(0x11, 0, 0, 0)  # Ctrl
    time.sleep(0.05)
    win32api.keybd_event(0x73, 0, 0, 0)  # F4
    time.sleep(0.05)
    win32api.keybd_event(0x73, 0, 2, 0)  # F4
    time.sleep(0.05)
    win32api.keybd_event(0x11, 0, 2, 0)  # Ctrl
    time.sleep(0.05)


def saveAsHTML(coord=DESKTOP_SIZE / 2, count=1):
    print "\n - SAVING HTML - "
    # move to center
    mousePos(coord=DESKTOP_SIZE / 2)
    rightClick()
    mousePos(coord=(coord + a(53, 65)))
    leftClick()
    # set text
    fileString = '{0}{1}_game{2}_stats{3:02d}.html'.format(desktop_path, year, last_game_number, count)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, unicode(fileString))
    win32clipboard.CloseClipboard()
    time.sleep(SLEEP)
    ctrlV()
    time.sleep(SLEEP)
    enter()

def doMainWindow():
    """StatMaster MAIN WINDOW """
    # print 'Click on Reports'
    mousePos(coord=a(84, 37))
    leftClick()

    # print 'Click on Organization'
    mousePos(coord=a(100, 69))
    leftClick()

    # print 'Click on Standard Reports'
    mousePos(coord=a(268, 69))
    leftClick()


def doDataDiskWindow():
    """ Select Data Disk popup"""
    # print 'Click on OK (in Select Data Disk)'
    mousePos(coord=a(1250, 280))
    leftClick()


def doReprtSelection():
    """Report Selection"""
    # print 'Click on Standings"
    mousePos(coord=a(685, 350))
    leftClick()
    # print 'Click on Team vs Team"
    mousePos(coord=a(685, 377))
    leftClick()
    # print 'Click on Batting Club"
    mousePos(coord=a(685, 540))
    leftClick()
    # print 'Click on Pitching Club"
    mousePos(coord=a(685, 570))
    leftClick()
    # print 'Click on Fielding Club"
    mousePos(coord=a(685, 600))
    leftClick()
    # print 'Click on Batting Leaders.."
    mousePos(coord=a(685, 675))
    leftClick()
    # print 'Click on Pitching Leaders.."
    mousePos(coord=a(685, 705))
    leftClick()
    # print 'Click on Relief Pitching Leaders.."
    mousePos(coord=a(685, 735))
    leftClick()
    # print 'Click on Display"
    mousePos(coord=a(1200, 350))
    leftClick()


def doSaveReports():
    """SAVE REPORTS"""
    for i in range(1, NUMBER_OF_REPORTS + 1):
        saveAsHTML(count=i)
        closeReport()


if __name__ == '__main__':
    # TODO: open StatMaster and maximize programatically
    doMainWindow()
    doDataDiskWindow()
    doReprtSelection()
    doSaveReports()
    # TODO: close StatMaster
    print "Finished"
