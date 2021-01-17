import win32clipboard, win32con
import time


def set_clipbaord(data):
    win32clipboard.OpenClipboard()
    time.sleep(0.1)
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()


def get_clipboard():
    data = None
    for i in range(10000):

        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            break
        except:
            #win32clipboard.CloseClipboard()
            time.sleep(0.01)
    return data

# def get_clipboard():
#     win32clipboard.OpenClipboard()
#     try:
#         text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
#     except (TypeError, win32clipboard.error):
#         try:
#             text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
#             text = py3compat.cast_unicode(text, py3compat.DEFAULT_ENCODING)
#         except (TypeError, win32clipboard.error):
#             raise ClipboardEmpty
#     finally:
#         win32clipboard.CloseClipboard()
#     print(text)
#     return text


def empty_clipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
