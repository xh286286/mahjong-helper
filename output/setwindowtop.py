import win32gui
import keyboard
import win32con
import winxpgui
import win32api

import atexit


filename = "C:\project\mahjong-helper\output\mahjong-helper.exe"
class totop:
    hw = ''
    
    topflag = False
    alphaflag = False

    def gethw(self):
        def foo(hwnd,mouse):
            if win32gui.GetWindowText(hwnd) ==  filename:
                self.hw = hwnd
        win32gui.EnumWindows(foo,0)

    def force_focus(self, hwnd):
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOOWNERZORDER | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        print("置顶", hwnd, win32gui.GetWindowText(hwnd))

    def cancel_focus(self, hwnd):
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        print("取消置顶", hwnd, win32gui.GetWindowText(hwnd))

    def transparent(self, hwnd):
        lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        lExStyle |=  win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE , lExStyle )
        winxpgui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 180, win32con.LWA_ALPHA)
        
    def untransparent(self, hwnd):
        lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if lExStyle & win32con.WS_EX_TRANSPARENT:
            lExStyle ^=  win32con.WS_EX_TRANSPARENT
        if lExStyle & win32con.WS_EX_LAYERED:
            lExStyle ^=  win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE , lExStyle )
        #winxpgui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 255, win32con.LWA_ALPHA)

    def handler(self, op, hwnd):
        op(hwnd)

    def get_key(self):
        def fun():
            if not self.topflag:  
                self.topflag = True
                self.gethw()
                if self.hw: 
                    self.handler(self.force_focus, self.hw)
            else:
                self.topflag = False
                self.gethw()
                if self.hw: 
                    self.handler(self.cancel_focus, self.hw)


        def fun1():
            if not self.alphaflag:  
                self.alphaflag = True
                self.gethw()
                if self.hw: 
                    print('make transparent')
                    self.transparent(self.hw)
                    self.title = win32gui.GetWindowText(self.hw)
                    print(self.title)
            else:
                self.alphaflag = False
                self.gethw()
                if self.hw: 
                    print('make opaque')
                    self.untransparent(self.hw)

        keyboard.add_hotkey('alt+t', fun)
        keyboard.add_hotkey('alt+e', fun1)


        while True:
            keyboard.wait()

import os
if __name__ == '__main__':

    #os.popen(filename)
    #os.system(filename)


    zd = totop()
    zd.get_key()