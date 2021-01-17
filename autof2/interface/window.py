from autof2.interface import clipboard
from autof2.interface import mouse
from autof2.interface.send_data import SendData

import win32con
import win32gui

F2_WINDOW_NAMES = (
    'Connect 2000 (© Uniware Computer Systems BV) (Session 1 : 192.168.180.1)',
    'Connect 2000 (© Uniware Computer Systems BV) (Session 2 : 192.168.180.1)',

)


def enumHandler(hwnd, lParam):
    global f2_hwnd
    if win32gui.IsWindowVisible(hwnd):
        if 'Connect 2000 (© Uniware Computer Systems BV) (Session 1 : 192.168.180.1)' in win32gui.GetWindowText(hwnd):
            f2_hwnd = hwnd


def Dutch_enumHandler(hwnd, lParam):
    global f2_hwnd
    if win32gui.IsWindowVisible(hwnd):
        if 'Connect 2000 (© Uniware Computer Systems BV) (Session 1 : connect.metz.com)' in win32gui.GetWindowText(
                hwnd):
            f2_hwnd = hwnd
        elif 'Connect (© Uniware Computer Systems BV) (Session 1 : connect.metz.com)' in win32gui.GetWindowText(hwnd):
            f2_hwnd = hwnd


def Canada_enumHandler(hwnd, lParam):
    global f2_hwnd
    if win32gui.IsWindowVisible(hwnd):
        if 'Connect 2000 (© Uniware Computer Systems BV) (Session 1 : 192.168.180.1)' in win32gui.GetWindowText(hwnd):
            f2_hwnd = hwnd


# def get_hwnd():
#    win32gui.EnumWindows(enumHandler, f2_hwnd) # stops when f2_hwnd is not None

def get_hwnd():
    win32gui.EnumWindows(Dutch_enumHandler, f2_hwnd)  # stops when f2_hwnd is not None


def get_corners(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x0 = rect[0]
    y0 = rect[1]
    x1 = rect[2]  # - x
    y1 = rect[3]  # - y

    return x0, y0, x1, y1


def drag_window():
    win32gui.ShowWindow(f2_hwnd, win32con.SW_MAXIMIZE)
    try:
        win32gui.SetForegroundWindow(f2_hwnd)
    except:
        get_hwnd()
        # win32gui.SetForegroundWindow(f2_hwnd)
    c = get_corners(f2_hwnd)
    border = 32
    mouse.click_and_drag(c[0] + border, c[1] + (border * 2), c[2] - border, c[3] - (border * 2))


def get_window():
    send = SendData()
    drag_window()
    send.send('%c')
    data = None
    for i in range(3):
        data = clipboard.get_clipboard()
        break
    return data


f2_hwnd = None
get_hwnd()
