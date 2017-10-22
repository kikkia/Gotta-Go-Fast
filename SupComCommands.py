from pymouse import PyMouse
from pykeyboard import PyKeyboard
import cv2
import numpy as np
import time
from threading import Thread
from Read import ReadValue
from Read import initRead

mouse = PyMouse()
k = PyKeyboard()

def SingleSelect(x, y):
    mouse.click(x, y)

def MultiSelect(startX, startY, endX, endY):
    mouse.move(startX,startY)
    mouse.drag(endX, endY)

def SimilarSelect(x, y):
    mouse.click(x, y, 1, 2)

def CommanderSelect():
    k.press_keys([k.alt_key, ','])

def EnginnerSelect():
    k.press_keys([k.alt_key, '.'])

def LandFactorySlect():
    k.press_keys([k.control_key,  k.shift_key, 'l'])

def AirFactorySlect():
    k.press_keys([k.control_key,  k.shift_key, 'a'])

def SeaFactorySlect():
    k.press_keys([k.control_key,  k.shift_key, 's'])

def Move(x,y):
    k.tap_key('m')
    mouse.click(x, y)

def Attack(x, y):
    k.tap_key('a')
    mouse.click(x, y)

def BuildPower(x,y):
    k.tap_key('b')
    k.tap_key('p')
    k.press_keys(k.shift_key)
    mouse.click(x,y)
    k.release_key(k.shift_key)
    k.tap_key(k.escape_key)


def ReadPower():
    ReadValue()

def ReadMass():
    ReadValue()

def ReadUnitCap():
    ReadValue()

def ReadResearch():
    ReadValue()

i=0
j=0
initRead()
while True:
    i+=1
    j+=1
    CommanderSelect()
    BuildPower(i,j)