#!/usr/bin/python
#

from os import system, name
import datetime

# define our clear function


def clearScreen():

    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')


def welcome():

    currentDT = datetime.datetime.now()

    print("Welcome to Payslipper")
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S"))
    print("")
