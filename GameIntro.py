import logging

import tkinter as tk

MAX_BOARD_SIZE = 50
MIN_BOARD_SIZE = 10
DEFAULT_WIDTH = 14
DEFAULT_HEIGHT = 14


class MainWindow:
    def __init__(self):
        self.frame = tk.Tk()

    @staticmethod
    def validation_check(val):
        if not val.get().isdigit():
            return False

        if MIN_BOARD_SIZE <= int(val.get()) <= MAX_BOARD_SIZE:
            return True

        return False

    def callback(self, val, entry):
        if not self.validation_check(val):
            entry.config({"background": '#c92508'})

        else:
            entry.config({"background": 'white'})

    @staticmethod
    def init_labels(frame):
        w_lab = tk.Label(frame, text='ENTER WIDTH: ')
        h_lab = tk.Label(frame, text='ENTER LENGTH: ')

        w_lab.grid(column=0, row=0)
        h_lab.grid(column=0, row=1)

    def init_entries(self, frame, width, height):
        w_entry = tk.Entry(frame, textvariable=width, width=4)
        h_entry = tk.Entry(frame, textvariable=height, width=4)
        w_entry.grid(column=1, row=0)
        h_entry.grid(column=1, row=1)

        width.trace("w", lambda name, index, mode, _width=width: self.callback(width, w_entry))
        height.trace("w", lambda name, index, mode, _height=height: self.callback(height, h_entry))


    def init(self, button_callback):

        width = tk.StringVar(value=DEFAULT_WIDTH)
        height = tk.StringVar(value=DEFAULT_HEIGHT)
        self.init_labels(self.frame)
        self.init_entries(self.frame, width, height)

        start_button = tk.Button(self.frame, text='CONFIRM', command=lambda: button_callback(self, width, height))

        start_button.grid_rowconfigure(0, weight=1)
        start_button.grid_columnconfigure(0, weight=1)
        start_button.grid(column=4, row=0, rowspan=3, sticky=tk.N + tk.S + tk.E + tk.W)
        return self.frame

    def exit(self):
        try:
            self.frame.destroy()
            return True
        except NameError:
            logging.warning('WINDOW CLOSE ERROR')
            return False

import ctypes

def start_button_callback(obj, w, h):
    _max = int(w.get()) * int(h.get())
    if not (obj.validation_check(w) and obj.validation_check(h)):
        ctypes.windll.user32.MessageBoxW(0, "ENTER CORRECT DATA", "ERROR", 1)
        return False

def main():
    main_window = MainWindow()
    main_window.init(start_button_callback).mainloop()


if __name__ == '__main__':
    main()