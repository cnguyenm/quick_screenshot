import os
import glob
import threading
import signal
import pyautogui
import keyboard
import tkinter as tk
from tkinter import filedialog
from balloontip import WindowsBalloonTip

class ScreenShotManager():

    def __init__(self):
        self.save_dir_path = './screenshot'  # default save dir
        self.count = 0  # number of ss in  dir
        self.noti = WindowsBalloonTip()
        self.__get_num_screenshot()
        self.__create_gui()
        
    def run(self):
        self.root.mainloop()
    
    def __take_screenshot(self):
        
        # if path not exist
        if not os.path.exists(self.save_dir_path):
            os.mkdir(self.save_dir_path)

        # take ss, most important func, tbh
        ss_path = "%s/ss%d.png" % (self.save_dir_path, self.count)
        my_screen_shot = pyautogui.screenshot()
        my_screen_shot.save(ss_path)
        print("save done:", ss_path)

        # update gui
        self.status_text.configure(state='normal')
        self.status_text.delete("1.0", tk.END)
        self.status_text.insert(tk.END, "Save done.\nFile:%s" % ss_path)
        self.status_text.configure(state='disabled')

        # window noti
        # self.noti.show(title, msg)
        title = "Quick screenshot"
        msg = "Save " + ss_path
        x = threading.Thread(target=self.noti.show, args=(title, msg))
        x.start()

        # update cur index
        self.count += 1

    def __get_num_screenshot(self):
        """
        get number of ss in save_dir to avoid overwrite\n
        and update cur_ss_index
        """

        # if doesn't exit
        if not os.path.exists(self.save_dir_path):
            self.count = 0
            return 
        
        # else, get number of png files
        self.count = len(glob.glob1(self.save_dir_path, "*.png"))
        self.count += 1

        print("current ss index:", self.count)

    def __ask_save_dir(self):
        # prompt ask
        self.save_dir_path = filedialog.askdirectory()

        # update text
        self.save_dir_text.configure(state='normal')
        self.save_dir_text.delete("1.0", tk.END)
        self.save_dir_text.insert(tk.END, "Save dir:\n%s" % self.save_dir_path)
        self.save_dir_text.configure(state='disabled')

        # update count
        self.__get_num_screenshot()

    def __create_gui(self):

        # main window
        self.root = tk.Tk()
        self.root.title("Quick screenshot")
        canvas1 = tk.Canvas(master=self.root, width=300, height=200)
        canvas1.pack()
        

        # text: status
        self.status_text = tk.Text(master=self.root, width=40, height=3)
        self.status_text.insert(tk.END, "Hello there\nStart by select your save dir")
        self.status_text.pack()
        self.status_text.configure(state='disabled')

        # text: cur_save_dir
        self.save_dir_text = tk.Text(master=self.root, width=40, height=4)
        self.save_dir_text.insert(tk.END, "Default save dir:\n%s" % self.save_dir_path)
        self.save_dir_text.pack()
        self.save_dir_text.configure(state='disabled')

        # checkbox
        self.use_keyboard = tk.BooleanVar()
        c1 = tk.Checkbutton(master=self.root, text='Use Ctrl+F11 for screenshot', variable=self.use_keyboard, command=self.__toggle_keyboard)
        c1.pack() 

        # btn: take screen shot
        screenshot_btn = tk.Button(master=self.root, text='Take screenshot', command=self.__take_screenshot)
        screenshot_btn.pack()

        # btn: save dir
        save_dir_btn = tk.Button(master=self.root, text='Select save dir', command=self.__ask_save_dir)
        save_dir_btn.pack()
    
    def __event_f12(self, event):
        self.__take_screenshot()

    def __toggle_keyboard(self):
        # register keyboard
        print("toggle keyboard:", self.use_keyboard.get())
        use = self.use_keyboard.get()
        if use:
            keyboard.add_hotkey('ctrl+f11', self.__take_screenshot)
        else:
            keyboard.unhook_all()

def sigint_handler(sig, frame):
    print("Ctrl+C interrupt. Quit")

    # just to be sure
    keyboard.unhook_all()
    exit(1)

# handle interrupt
signal.signal(signal.SIGINT, sigint_handler)

# run program
ScreenShotManager().run()
