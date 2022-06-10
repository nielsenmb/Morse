from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from argparse import ArgumentParser
import sys, glob, os
import pandas as pd
#from PyQt5 import QtCore, QtGui

app = None

class MyMainWindow(QMainWindow):
    def __init__(self, df, dfpath, image_dir, app, shuffle=True):
        super().__init__()

        if shuffle:
            self.df = df.sample(frac=1).reset_index(drop=True)
        else:
            self.df = df

        self.dfpath = dfpath
        self.image_dir = image_dir
        self.app = app
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle('Inspector')

        self.setFixedWidth(1700)
        self.setFixedHeight(1000)

        #self.move(50, 50)
        
        central_widget = MyCentralWidget(self, self.app)
        
        self.setCentralWidget(central_widget)
        
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

        smplMod_button = QPushButton('Sample models (&C)', self)
        smplMod_button.setShortcut('C')
        smplMod_button.clicked.connect(self.on_smplMod_button_clicked)
        
        prMod_button = QPushButton('Prior model (&V)', self)
        prMod_button.setShortcut('V')
        prMod_button.clicked.connect(self.on_prMod_button_clicked)
        

 

        goodFit_button = QPushButton('Good (&G)', self)
        goodFit_button.setShortcut('G')
        goodFit_button.clicked.connect(self.on_osc_button_clicked)

        badFit_button = QPushButton('Bad (&B)', self)
        badFit_button.setShortcut('B')
        badFit_button.clicked.connect(self.on_no_button_clicked)
        
        hm_button = QPushButton('Hmmm (&H)', self)
        hm_button.setShortcut('H')
        hm_button.clicked.connect(self.on_hm_button_clicked)

        skip_button = QPushButton('Sad bad data (&S)', self)
        skip_button.setShortcut('S')
        skip_button.clicked.connect(self.on_skip_button_clicked)
        

        # define label
        self.label = QLabel(self)
        self.my_widget = MyWidget(self.label, self.main_window.df, self.main_window.image_dir)

        # Place the buttons - HZ
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(smplMod_button)
        hbox.addWidget(prMod_button)
        hbox.addStretch(1)
        hbox.addWidget(goodFit_button)
        hbox.addWidget(badFit_button)
        hbox.addWidget(skip_button)
        hbox.addWidget(hm_button)

        hbox.addStretch(1)

        # place hbox and label into vbox
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.next_image()

    def next_image(self):

        self.idx += 1

        while self.main_window.df.loc[self.idx].flag >= 0:

            self.idx += 1

            if (self.idx in self.main_window.df.index) == False:
                print('Finished going through CSV file')
                print('If any unclassified targets remain, they may not have associated png files')
                sys.exit()

        id = self.main_window.df.loc[self.idx].ID
        
        # There are two naming policies for pbjam figures currently in circulation
        # This just checks for both of them.
        self.smplModImg = glob.glob(os.path.join(*[self.main_window.image_dir, f'{id}_samples_model.png']))

        self.prModImg = glob.glob(os.path.join(*[self.main_window.image_dir, f'{id}_prior_model.png']))
        

        if len(self.smplModImg)==0:
            self.my_widget.show_image(os.path.join(*[os.getcwd(),'failed.jpg']))
            mess = f"{id}_samples_model.png not found, so I skipped it"
            print(mess)
            self.write_verdict(-1, mess)
        else:    
            self.my_widget.show_image(self.smplModImg[0])
             
            

    def on_smplMod_button_clicked(self):
        self.my_widget.show_image(self.smplModImg[0])

    def on_prMod_button_clicked(self):
           if len(self.prModImg) == 0:
               id = self.main_window.df.loc[self.idx].ID
               message = f'No prior model plot for {id}'
               self.main_window.statusBar().showMessage(message)
           else:
               try:
                   self.my_widget.show_image(self.prModImg[0])
               except:
                   message = f'Failed to load prior model plot for {id}'
                   self.main_window.statusBar().showMessage(message)
                   
  

    def on_osc_button_clicked(self):
        self.write_verdict(1, 'Last star was good')

    def on_no_button_clicked(self):
        self.write_verdict(0, 'Last star was bad')

    def on_skip_button_clicked(self):
        self.write_verdict(-1, 'Skipping image.')
        
    def on_hm_button_clicked(self):
        self.write_verdict(2, 'Last star was a hm')
 
        

    def write_verdict(self, code, mess):
        self.main_window.df.at[self.idx, 'flag'] = code
        perc = '%i / %i' % (self.idx, len(self.main_window.df))
        self.main_window.statusBar().showMessage(perc + ' - ' + mess)
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

def main(df, dfpath, image_dir, shuffle=True):
    '''
    app must be defined already!!!
    '''
    global app
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    w = MyMainWindow(df, dfpath, image_dir, app, shuffle=shuffle)
    w.show()
    app.exit(app.exec_())

parser = ArgumentParser()
parser.add_argument('target_list', type=str)
parser.add_argument('image_dir', type=str)
parser.add_argument('--shuffle', action='store_true', dest='shuffle',
                    help="shuffle the list of targets")
parser.add_argument('--no-shuffle', action='store_false', dest='shuffle',
                    help="don't shuffle the list of targets (default)")
parser.set_defaults(feature=False)

if __name__ == "__main__":
    args = parser.parse_args()

    df = pd.read_csv(args.target_list, converters={'ID': str, 'flag': int})

    if len(df) > 100:
        sys.setrecursionlimit(len(df))

    if not 'ID' in df.columns:
        print('CSV file must contain a column named ID')
        sys.exit()

    if not 'flag' in df.columns:
        df['flag'] = [-1 for n in range(len(df))]

    main(df, args.target_list, args.image_dir, shuffle=args.shuffle)
