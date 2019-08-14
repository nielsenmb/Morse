#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
import sys
import pandas as pd
import glob
import os

app = None

class MyMainWindow(QMainWindow):
    def __init__(self, df, dfpath, image_dir, app):
        super().__init__()
        self.df = df  
        self.dfpath = dfpath
        self.image_dir = image_dir
        self.app = app
        self.initUI()

    def initUI(self):
        self.resize(1600,900)
        self.move(50,50)
        central_widget = MyCentralWidget(self, self.app)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('ATL inspector')
        self.statusBar().showMessage('Waiting...')

    def auto(self):
        self.central_widget.auto()

class MyCentralWidget(QWidget):

    def __init__(self, main_window, app):
        super().__init__()
        self.main_window = main_window
        self.idx = -1
        self.app = app
        self.initUI()


    def initUI(self):
        good_button = QPushButton('&Good', self)
        good_button.setShortcut('g')
        good_button.clicked.connect(self.on_good_button_clicked)
        
        may_button = QPushButton('&Maybe', self)
        may_button.setShortcut('m')
        may_button.clicked.connect(self.on_may_button_clicked)
        
        bad_button = QPushButton('&Bad', self)
        bad_button.setShortcut('b')
        bad_button.clicked.connect(self.on_bad_button_clicked)
        
        # define label
        self.label = QLabel(self)
        self.my_widget = MyWidget(self.label, self.main_window.df, self.main_window.image_dir)
        
        # Place the buttons - HZ
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(good_button)
        hbox.addWidget(may_button)
        hbox.addWidget(bad_button)
        hbox.addStretch(1)
        
        # place hbox and label into vbox
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.next_image()

    def next_image(self):
        
        self.idx += 1
                
        while self.main_window.df.loc[self.idx].verdict_code >= 0:

            self.idx += 1
            
            if (self.idx in self.main_window.df.index) == False:
                print('Finished going through CSV file')
                print('If any unclassified targets remain, they may not have associated png files')
                sys.exit()       
                   
        id = str(int(self.main_window.df.loc[self.idx].ID))   
               
        sfile = glob.glob(os.path.join(*[self.main_window.image_dir,'*%s*.png' % (id)]))

        if len(sfile)==0:
            self.my_widget.show_image(os.path.join(*[os.getcwd(),'failed.jpg']))
            print("*%s*.png not found, so I skipped it" % (id))
            self.write_verdict(-1, "*%s*.png not found, so I skipped it" % (id))
        else:
            self.my_widget.show_image(sfile[0])

            
    def on_good_button_clicked(self):
        self.write_verdict(2, 'Last jam was Good')
        
    def on_bad_button_clicked(self):
        self.write_verdict(0, 'Last jam was Bad')
        
    def on_may_button_clicked(self):
        self.write_verdict(1, 'Last jam was Maybe')
    
    def write_verdict(self, err_code, mess):
        self.main_window.df.at[self.idx, 'verdict_code'] = err_code
        self.main_window.statusBar().showMessage(mess)
        self.main_window.df.to_csv(self.main_window.dfpath, index=False)

        if self.idx < len(self.main_window.df) - 1:
            self.next_image()
        else:
            self.main_window.statusBar().showMessage('Finished')
            sys.exit()
    
class MyWidget():
    def __init__(self, label, df, image_dir):
        self.label = label

    def show_image(self, sfile):
        pixmap = QPixmap(sfile)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

def main(df, dfpath, image_dir):
    '''
    app must be defined already!!!
    '''
    global app
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    w = MyMainWindow(df, dfpath, image_dir, app)
    w.show()
    app.exit(app.exec_())

if __name__ == "__main__":
    if len(sys.argv) == 3:
        df = pd.read_csv(sys.argv[1])#.sample(frac=1).reset_index(drop=True)
        if df.columns.contains('verdict_code') == False:
            df['verdict_code'] = [-1 for n in range(len(df))]
        dfpath = sys.argv[1]
        file_dir = sys.argv[2]
        main(df, dfpath, file_dir)
    else:
        print('Usage: inspector.py <targets.csv> <image_dir>')
