import ctypes
import ctypes.wintypes
from ctypes import *
import os

dll_path = os.path.join(os.path.dirname(__file__), 'PyGUIBuilder.dll')

mygui_dll = ctypes.CDLL(dll_path)

HWND = c_int

class Window_t(Structure):
    _fields_ = [("hwnd", c_void_p),
                ("hInstance", c_void_p),
                ("width", c_int),
                ("height", c_int)]

mygui_dll.createWindow_dll.argtypes = [c_char_p, c_char_p, c_int, c_int]
mygui_dll.createWindow_dll.restype = Window_t

mygui_dll.createLabel_dll.argtypes = [Window_t, c_char_p, c_int, c_int]
mygui_dll.createLabel_dll.restype = c_void_p

mygui_dll.createButton_dll.argtypes = [Window_t, c_char_p, CFUNCTYPE(None), c_int, c_int]
mygui_dll.createButton_dll.restype = c_void_p

mygui_dll.createEntry_dll.argtypes = [Window_t, c_char_p, c_int, c_int]
mygui_dll.createEntry_dll.restype = c_void_p

mygui_dll.clearText_dll.argtypes = [HWND]
mygui_dll.clearText_dll.restype = None

mygui_dll.getText_dll.argtypes = [HWND]
mygui_dll.getText_dll.restype = c_char_p

mygui_dll.setText_dll.argtypes = [HWND, c_char_p]
mygui_dll.setText_dll.restype = None

mygui_dll.showMessageBox_dll.argtypes = [c_char_p, c_char_p, c_char_p]
mygui_dll.showMessageBox_dll.restype = c_int

mygui_dll.createComboBox_dll.argtypes = [Window_t, POINTER(c_char_p), c_int, c_int, c_int]
mygui_dll.createComboBox_dll.restype = c_void_p

mygui_dll.getComboBoxSelection_dll.argtypes = [c_void_p]
mygui_dll.getComboBoxSelection_dll.restype = c_char_p

# Define MessageBox return values
IDOK = 1
IDCANCEL = 2
IDABORT = 3
IDRETRY = 4
IDIGNORE = 5
IDYES = 6
IDNO = 7

def createWindow(title, icon, width, height):
    return mygui_dll.createWindow_dll(title.encode('utf-8'), icon.encode('utf-8'), width, height)

def createLabel(window, text, row, column):
    return mygui_dll.createLabel_dll(window, text.encode('utf-8'), row, column)

ButtonCallback = CFUNCTYPE(None)

_global_callbacks = []

def createButton(window, text, callback, row, column):
    callback_c = ButtonCallback(callback)
    _global_callbacks.append(callback_c)
    return mygui_dll.createButton_dll(window, text.encode('utf-8'), callback_c, row, column)

def createEntry(window, text, row, column):
    return mygui_dll.createEntry_dll(window, text.encode('utf-8'), row, column)

def clearText(hwnd):
    return mygui_dll.clearText_dll(hwnd)

def getText(hwnd):
    text = mygui_dll.getText_dll(hwnd)
    return text.decode('utf-8')

def setText(hwnd, text):
    mygui_dll.setText_dll(hwnd, text.encode('utf-8'))

def destroyElement(hwnd):
    ctypes.windll.user32.DestroyWindow(hwnd)

def showMessageBox(type, title, message):
    
    result = mygui_dll.showMessageBox_dll(type.encode('utf-8'), title.encode('utf-8'), message.encode('utf-8'))
    
    if result == IDOK:
        return "OK"
    elif result == IDCANCEL:
        return "Cancel"
    elif result == IDYES:
        return "Yes"
    elif result == IDNO:
        return "No"
    elif result == IDRETRY:
        return "Retry"
    elif result == IDABORT:
        return "Abort"
    elif result == IDIGNORE:
        return "Ignore"
    else:
        return "Unknown"

def createComboBox(window, options, row, column):
    options_c = (c_char_p * len(options))(*[opt.encode('utf-8') for opt in options])
    return mygui_dll.createComboBox_dll(window, options_c, len(options), row, column)

def getComboBoxSelection(comboBox):
    return mygui_dll.getComboBoxSelection_dll(comboBox).decode('utf-8')

def run():
    msg = ctypes.wintypes.MSG()
    while True:
        ret = ctypes.windll.user32.GetMessageW(ctypes.pointer(msg), None, 0, 0)
        if ret == 0:
            break
        ctypes.windll.user32.TranslateMessage(ctypes.pointer(msg))
        ctypes.windll.user32.DispatchMessageW(ctypes.pointer(msg))
