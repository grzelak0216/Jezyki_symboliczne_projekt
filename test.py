import tkinter
import pygame
import unittest
from Main import MainWindow, start_button_callback

class Test_tkinter (unittest.TestCase):
    def test_get_correct_size_11x13(self):
        mainwindow = MainWindow()
        w = tkinter.StringVar(value = 11)
        h = tkinter.StringVar(value = 13)
        wt, wh = start_button_callback(mainwindow, w, h)
        self.assertEqual((wt, wh), (11, 13))
        pygame.quit()

    def test_get_correct_size_21x11(self):
        mainwindow = MainWindow()
        w = tkinter.StringVar(value = 21)
        h = tkinter.StringVar(value = 11)
        wt, wh = start_button_callback(mainwindow, w, h)
        self.assertEqual((wt, wh), (21, 11))
        pygame.quit()

    def test_bad_size_other(self):
        mainwindow = MainWindow()
        w = tkinter.StringVar(value = 3)
        h = tkinter.StringVar(value = 50)
        flag = start_button_callback(mainwindow, w, h)
        self.assertEqual(flag, False)
        pygame.quit()

    def test_bad_size_zero(self):
        mainwindow = MainWindow()
        w = tkinter.StringVar(value = 20)
        h = tkinter.StringVar(value = 0)
        flag = start_button_callback(mainwindow, w, h)
        self.assertEqual(flag, False)
        pygame.quit()

    def test_bad_size_over(self):
        mainwindow = MainWindow()
        w = tkinter.StringVar(value = 100)
        h = tkinter.StringVar(value = 50)
        flag = start_button_callback(mainwindow, w, h)
        self.assertEqual(flag, False)
        pygame.quit()

class Test_pygame (unittest.TestCase):
    def test_enter_exit(self):
        mainwindow = MainWindow()
        w = tkinter.StringVar(value=11)
        h = tkinter.StringVar(value=11)

