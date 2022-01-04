import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import random

import os
import socket
import patoolib
import datetime
# definisikan IP untuk binding
TCP_IP = "192.168.1.18"
# definisikan port untuk binding
TCP_PORT = 5005
# definisikan ukuran buffer untuk menerima pesan
BUFFER_SIZE = 1024


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("launcher.ui",self)
        self.curr_var = "0.0.0"
        

        self.updateButton.clicked.connect(self.updateProgram)
        self.playButton.clicked.connect(self.playProgram)
        try:
            with open('undercover.rar.log', 'r') as f:
                    last_line = f.readlines()[-1]
                    self.curr_var = last_line[27:]
        except:
            print("version.log not found, creating version.log")
        finally:
            with open('undercover.rar.log', "a") as myfile:
                ct = datetime.datetime.now()
                log_ver = "\n" + str(ct) + " " + self.curr_var
                myfile.write(log_ver)
        self.versionLabel.setText(self.curr_var)

    def updateProgram(self):
        
        file_download = "undercover.rar"
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
        #if 1:
            s.connect((TCP_IP,TCP_PORT))
            new_ver = s.recv(BUFFER_SIZE)
            print("The newest version for the app is version",str(new_ver,'utf-8'))

            file_log = file_download + '.log'
            
            if(str(new_ver,'utf-8') != self.curr_var):
                print("Updating to",str(new_ver,'utf-8'))
                f = open(file_download,"wb+")
                broke = False
                # loop forever
                while 1:
                    # terima pesan dari server
                    data = s.recv(BUFFER_SIZE)
                    # tulis pesan yang diterima dari server ke file telah dibuka sebelumnya (hasil_download.txt)
                    try:
                        f.write(data)
                    except:
                        broke = True
                        print("Failed to update.")
                        break
                    if  not data: 
                        break
                f.close()
                if not broke:
                    print("Finished updating")
                    with open(file_log, "a") as myfile:
                        ct = datetime.datetime.now()
                        log_ver = "\n" + str(ct) + " " + str(new_ver,'utf-8')
                        myfile.write(log_ver)
                    self.curr_var = str(new_ver,'utf-8')
                    self.versionLabel.setText(self.curr_var)
                    mypath = os.path.abspath(os.path.dirname(__file__))
                    patoolib.extract_archive(file_download,outdir=mypath,interactive=False)
            else: print("You are up to date!")
        except:
            print("Connection Failed. Check your server")
        #tutup socket
        s.close()

    def playProgram(self):
        mypath = os.path.abspath(os.path.dirname(__file__))
        os.system( f'"{mypath}/main.exe"' )

app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()

#setup pages
mainwindow=MainWindow()
widget.addWidget(mainwindow)

widget.show()
app.exec()