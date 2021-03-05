import PIL
import numpy
import win32api, win32con
import os
import time

SLEEP = 0.5
MAG = 1.25

desktop_path = r"\\CNOCMF01\Staff_C$\rwconner\Desktop"

def left_Click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(SLEEP)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(SLEEP)
    print "Left Click."  # completely optional. But nice for debugging purposes.

def right_Click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(SLEEP)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
    time.sleep(SLEEP)
    print "Right Click."  # completely optional. But nice for debugging purposes.

def mouse_Pos(cord=(0, 0)):
    win32api.SetCursorPos((int(cord[0]/MAG), int(cord[1]/MAG)))
    time.sleep(SLEEP)

def save_As_HTML(cord=(0, 0)):
    mouse_Pos(cord=cord)
    right_Click()
    mouse_Pos(cord=cord+(62, 62))
    left_Click()

# With StatMaster Open...

# Click on Reports
mouse_Pos(cord=(84, 41))
left_Click()

# Click on Organization
mouse_Pos(cord=(115, 69))
left_Click()

# Click on Standard Reports
mouse_Pos(cord=(304, 69))
left_Click()

# Click on OK (in Select Data Disk)
mouse_Pos(cord=(1190, 380))
left_Click()

# Select the Summary Data
# Standings
mouse_Pos(cord=(685, 350))
left_Click()
# Team vs Team
mouse_Pos(cord=(685, 377))
left_Click()
# Batting Club
mouse_Pos(cord=(685, 540))
left_Click()
# Pitching Club
mouse_Pos(cord=(685, 570))
left_Click()
# Fielding Club
mouse_Pos(cord=(685, 600))
left_Click()
# Batting Leaders..
mouse_Pos(cord=(685, 675))
left_Click()
# Pitching Leaders..
mouse_Pos(cord=(685, 705))
left_Click()
# Relief Pitching Leaders..
mouse_Pos(cord=(685, 735))
left_Click()
# Display
mouse_Pos(cord=(1200, 350))
left_Click()

# Begin Saving

#NOTE: Maximise report will maximise all.

