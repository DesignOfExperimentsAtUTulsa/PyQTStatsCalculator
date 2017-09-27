"""
@author: Anvar Akhiiartdinov
"""

import sys
from PyQt5.QtCore import QCoreApplication, Qt, QModelIndex
from PyQt5.QtGui import *
from PyQt5.QtGui import (QIcon,QIntValidator,QDoubleValidator)
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, 
                            QTableWidget, QGridLayout, QTableWidgetItem, QGroupBox, QHBoxLayout,
                            QVBoxLayout, QLabel, QSizePolicy, QCheckBox, QInputDialog, 
                            QMessageBox, QAbstractButton, QSlider, QLineEdit)
import numpy as np
from scipy import stats

import os
 
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.mlab as mlab

rcParams.update({'figure.autolayout': True})

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        FigureCanvas.mpl_connect(self,'button_press_event', self.export)
        
    def export(self,event):
        if event.dblclick:
            filename = "ExportedGraph.pdf"
            self.fig.savefig(filename)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Saved a copy of the graphics window to {}".format(filename))
            msg.setWindowTitle("Saved PDF File")
            msg.setDetailedText("The full path of the file is \n{}".format(os.path.abspath(os.getcwd())))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowModality(Qt.ApplicationModal)
            msg.exec_()
            print("Exported PDF file")
        
class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.axes.set_xlabel("X Label")
        self.axes.set_ylabel("Y Label")
        self.axes.set_title("Title")
        self.axes.grid(True)
          
    def plot_t(self,df,alpha,t0,tsig):
        self.axes.clear()
        xmin = -4
        xmax = 4
        x = np.linspace(xmin,xmax, 100) #x = np.linspace(loc-3*scale,loc+3*scale, 100)
        y = stats.t.pdf(x,df)
        self.axes.set_xlabel("Student-t")
        self.axes.set_ylabel("PDF")
        self.axes.set_title("Two-Sided t-test for $\\alpha=%g$" %alpha)
        self.axes.plot(x,y,label='t distribution\nwith $\\nu=%g$' %df)
        self.axes.plot(t0,0.0,'+',color='k',label='Test Statistic',markersize=18)
        self.axes.legend(loc=0,shadow=True)
        arrowproperties = dict(width=2, headwidth=6, frac=0.2, facecolor='red',
                          shrink=0.1)
        self.axes.annotate('$t_0 = %0.3f $' %t0, xy=(t0,0), xytext=(t0,.1), xycoords='data', fontsize=
                           10,arrowprops=arrowproperties)
        
        lowerFilledX = np.arange(xmin,-tsig,.01)
        lowerFilledY = stats.t.pdf(lowerFilledX, df)
        self.axes.fill_between(lowerFilledX,0,lowerFilledY, label='Lower Tail', color='green' )
        upperFilledX = np.arange(tsig,xmax,.01)
        upperFilledY = stats.t.pdf(upperFilledX, df)
        self.axes.fill_between(upperFilledX,0,upperFilledY, label='Upper Tail', color='green' )
        self.axes.grid(True)        
        self.draw()
   
class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle('Stats_Graph_Anvar Akhiiartdinov')
        
        extractAction = QAction('&Exit', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('leave the app')
        extractAction.triggered.connect(self.close_application)
        
        extractAction1 = QAction('&Open .CSV', self)
        extractAction1.setShortcut('Ctrl+O')
        extractAction1.setStatusTip('Open .CSV file')
        extractAction1.triggered.connect(self.open_file)
        
        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction1)
        fileMenu.addAction(extractAction)
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.graph_canvas = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        
        #Given data
        self.table_checkbox = QCheckBox('Calculation from table',self.main_widget)
        self.table_checkbox.stateChanged.connect(self.compute_stats)
        self.stat_given_checkbox = QCheckBox('Calculation from given statistics',self.main_widget)
        self.stat_given_checkbox.stateChanged.connect(self.compute_stats)
        checks_layout = QHBoxLayout()
        checks_layout.addWidget(self.table_checkbox)
        checks_layout.addWidget(self.stat_given_checkbox)
                
        self.data_table = QTableWidget(self.main_widget)  
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        self.mean_sam1_freeze_label = QLabel("Mean of Sample 1", self.main_widget)                
        self.mean_sam1_edit = QLineEdit("16.76",self.main_widget)
        self.mean_sam1_edit.setValidator(QDoubleValidator())
        self.mean_sam1_edit.setMaxLength(5)
        self.mean_sam1_edit.resize(10,20)
        self.mean_sam2_freeze_label = QLabel("Mean of Sample 2", self.main_widget)    
        self.mean_sam2_edit = QLineEdit("17.04",self.main_widget)
        self.mean_sam2_edit.setValidator(QDoubleValidator())
        self.mean_sam2_edit.setMaxLength(5)
        self.mean_sam2_edit.resize(10,20)
                 
        self.std_sam1_freeze_label = QLabel("Std of Sample 1", self.main_widget)
        self.std_sam1_edit = QLineEdit("0.316",self.main_widget)
        self.std_sam1_edit.setValidator(QDoubleValidator())
        self.std_sam1_edit.setMaxLength(5)
        self.std_sam1_edit.resize(10,20)
        self.std_sam2_freeze_label = QLabel("Std of Sample 2", self.main_widget)
        self.std_sam2_edit = QLineEdit("0.248",self.main_widget)
        self.std_sam2_edit.setValidator(QDoubleValidator())
        self.std_sam2_edit.setMaxLength(5)
        self.std_sam2_edit.resize(10,20)
        
        self.num_sam1_freeze_label = QLabel("Num El of Sample 1", self.main_widget)
        self.num_sam1_edit = QLineEdit("10",self.main_widget)
        self.num_sam1_edit.setValidator(QIntValidator())
        self.num_sam1_edit.setMaxLength(3)
        self.num_sam1_edit.resize(10,20)
        self.num_sam2_freeze_label = QLabel("Num El of Sample 2", self.main_widget)
        self.num_sam2_edit = QLineEdit("10",self.main_widget)
        self.num_sam2_edit.setValidator(QIntValidator())
        self.num_sam2_edit.setMaxLength(3)
        self.num_sam2_edit.resize(10,20)
        
        sam1_layout = QVBoxLayout()
        sam1_layout.addWidget(self.mean_sam1_freeze_label)
        sam1_layout.addWidget(self.mean_sam1_edit)
        sam1_layout.addWidget(self.std_sam1_freeze_label)
        sam1_layout.addWidget(self.std_sam1_edit)
        sam1_layout.addWidget(self.num_sam1_freeze_label)
        sam1_layout.addWidget(self.num_sam1_edit)
        
        sam2_layout = QVBoxLayout()
        sam2_layout.addWidget(self.mean_sam2_freeze_label)
        sam2_layout.addWidget(self.mean_sam2_edit)
        sam2_layout.addWidget(self.std_sam2_freeze_label)
        sam2_layout.addWidget(self.std_sam2_edit)
        sam2_layout.addWidget(self.num_sam2_freeze_label)
        sam2_layout.addWidget(self.num_sam2_edit)
        
        sams_layout = QHBoxLayout()
        sams_layout.addLayout(sam1_layout)
        sams_layout.addLayout(sam2_layout)
        
        data_layout = QVBoxLayout()
        data_layout.addLayout(checks_layout)
        data_layout.addWidget(self.data_table)
        data_layout.addLayout(sams_layout)
                
        table_box = QGroupBox("Data Given")
        table_box.setLayout(data_layout)
        
        #Summary of statistics   
        self.mean_sam1_label_dub = QLabel("Mean of Sample 1", self.main_widget)                
        self.mean_sam1_label = QLabel("Not retrieved", self.main_widget)
        self.std_sam1_label_dub = QLabel("Std of Sample 1", self.main_widget)   
        self.std_sam1_label = QLabel("Not retrieved", self.main_widget)
        self.num_sam1_label_dub = QLabel("Num El of Sample 1", self.main_widget)   
        self.num_sam1_label = QLabel("Not retrieved", self.main_widget)
        stats1_layout = QVBoxLayout()
        stats1_layout.addWidget(self.mean_sam1_label_dub)
        stats1_layout.addWidget(self.mean_sam1_label)
        stats1_layout.addWidget(self.std_sam1_label_dub)
        stats1_layout.addWidget(self.std_sam1_label)
        stats1_layout.addWidget(self.num_sam1_label_dub)
        stats1_layout.addWidget(self.num_sam1_label)
        
        self.mean_sam2_label_dub = QLabel("Mean of Sample 2", self.main_widget)       
        self.mean_sam2_label = QLabel("Not retrieved", self.main_widget)
        self.std_sam2_label_dub = QLabel("Std of Sample 2", self.main_widget)       
        self.std_sam2_label = QLabel("Not retrieved", self.main_widget)
        self.num_sam2_label_dub = QLabel("Num El of Sample 2", self.main_widget)       
        self.num_sam2_label = QLabel("Not retrieved", self.main_widget)
        stats2_layout = QVBoxLayout()
        stats2_layout.addWidget(self.mean_sam2_label_dub)
        stats2_layout.addWidget(self.mean_sam2_label)
        stats2_layout.addWidget(self.std_sam2_label_dub)
        stats2_layout.addWidget(self.std_sam2_label)
        stats2_layout.addWidget(self.num_sam2_label_dub)
        stats2_layout.addWidget(self.num_sam2_label)
        
        stats_layout = QHBoxLayout()
        stats_layout.addLayout(stats1_layout)
        stats_layout.addLayout(stats2_layout)
        stats_box = QGroupBox("Summary Statistics")
        stats_box.setLayout(stats_layout)
        
        #Canvas area
        canvas_box = QGroupBox("Plotting Area")
        canvas_box_layout = QVBoxLayout()
        canvas_box_layout.addWidget(self.graph_canvas)
        canvas_box.setLayout(canvas_box_layout)
        
        #Calculation area
        self.calc_button = QPushButton("Calculate", self.main_widget)
        self.calc_button.clicked.connect(self.calculation)
        
        self.siglevel_label_freeze = QLabel("Significance level", self.main_widget)
        self.siglevel_edit = QLineEdit("0.05",self.main_widget)
        self.siglevel_edit.setValidator(QDoubleValidator())
        self.siglevel_edit.setMaxLength(4)
        self.siglevel_edit.resize(10,20)
        
        sig_layout = QHBoxLayout()
        sig_layout.addWidget(self.siglevel_label_freeze)
        sig_layout.addWidget(self.siglevel_edit)
                
        self.meandif_label_freeze = QLabel("Mean Dif", self.main_widget)
        self.meandif_label = QLabel("Not calculated", self.main_widget)
        self.sp_label_freeze = QLabel("Sp", self.main_widget)
        self.sp_label = QLabel("Not calculated", self.main_widget)
        self.stderr_label_freeze = QLabel("Std Error", self.main_widget)
        self.stderr_label = QLabel("Not calculated", self.main_widget)
        self.tsig_label_freeze = QLabel("t-value @ Sig level", self.main_widget)
        self.tsig_label = QLabel("Not calculated", self.main_widget)
        self.t0_label_freeze = QLabel("t0", self.main_widget)
        self.t0_label = QLabel("Not calculated", self.main_widget)
        self.p_label_freeze = QLabel("P-value", self.main_widget)
        self.p_label = QLabel("Not calculated", self.main_widget)
        self.lowerCI_label_freeze = QLabel("Lower CI", self.main_widget)
        self.lowerCI_label = QLabel("Not calculated", self.main_widget)
        self.upperCI_label_freeze = QLabel("Upper CI", self.main_widget)
        self.upperCI_label = QLabel("Not calculated", self.main_widget)
               
        calc_freeze_layout = QVBoxLayout()
        calc_freeze_layout.addWidget(self.meandif_label_freeze)
        calc_freeze_layout.addWidget(self.sp_label_freeze)
        calc_freeze_layout.addWidget(self.stderr_label_freeze)
        calc_freeze_layout.addWidget(self.tsig_label_freeze)
        calc_freeze_layout.addWidget(self.t0_label_freeze)
        calc_freeze_layout.addWidget(self.p_label_freeze)
        calc_freeze_layout.addWidget(self.lowerCI_label_freeze)
        calc_freeze_layout.addWidget(self.upperCI_label_freeze)
        
        calc_layout = QVBoxLayout()
        calc_layout.addWidget(self.meandif_label)
        calc_layout.addWidget(self.sp_label)
        calc_layout.addWidget(self.stderr_label)
        calc_layout.addWidget(self.tsig_label)
        calc_layout.addWidget(self.t0_label)
        calc_layout.addWidget(self.p_label)
        calc_layout.addWidget(self.lowerCI_label)
        calc_layout.addWidget(self.upperCI_label)
        
        hor_layout = QHBoxLayout()
        hor_layout.addLayout(calc_freeze_layout)
        hor_layout.addLayout(calc_layout)
        
        ver_layout = QVBoxLayout()
        ver_layout.addWidget(self.calc_button)
        ver_layout.addLayout(sig_layout)
        ver_layout.addLayout(hor_layout)
        calc_box = QGroupBox("Calculation Area")
        calc_box.setLayout(ver_layout)
        
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(canvas_box,0,1) 
        grid_layout.addWidget(calc_box,1,1) 
                
        self.main_widget.setLayout(grid_layout)
                
        self.show()
        
                        
    def close_application(self):
        print('exit')
        sys.exit()
        
    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file',
                                              'Home/', '*.csv')
       
        print('filename', filename, '\n')
        with open(filename[0],'r') as data_file:
            self.data_lines = data_file.readlines()
           
        print("Opened {}".format(filename[0]))
        print(self.data_lines[1:10])
                
        header_row = 0 
        self.data_table_columns = self.data_lines[header_row].strip().split(',')
        self.data_table.setColumnCount(len(self.data_table_columns))
        self.data_table.setHorizontalHeaderLabels(self.data_table_columns)
        
        current_row = -1
        for row in range(header_row+1, len(self.data_lines)):
            row_values = (self.data_lines[row].strip().split(','))
            current_row +=1
            self.data_table.insertRow(current_row)
            for col in range(len(self.data_table_columns)):
                entry = QTableWidgetItem("{}".format(row_values[col]))
                self.data_table.setItem(current_row,col,entry)
        print("Filled {} rows.".format(row))
        
    def compute_stats(self):
        
        if self.table_checkbox.isChecked():
            sample1_list=[]
            sample2_list=[]
            for row in range(self.data_table.rowCount()):
                sample1_list.append(float(self.data_table.item(row,1).text()))
                sample2_list.append(float(self.data_table.item(row,2).text()))
            
            sam1_array = np.asarray(sample1_list)
            self.mean_sam1 = np.mean(sam1_array)
            self.stdev_sam1 = np.std(sam1_array)
            self.num_sam1 = len(sam1_array)
            
            sam2_array = np.asarray(sample2_list)
            self.mean_sam2 = np.mean(sam2_array)
            self.stdev_sam2 = np.std(sam2_array)
            self.num_sam2 = len(sam2_array)
            
        if self.stat_given_checkbox.isChecked():
            self.mean_sam1 = self.mean_sam1_edit.text()
            self.mean_sam1 = float(self.mean_sam1)
            self.stdev_sam1 = self.std_sam1_edit.text()
            self.stdev_sam1 = float(self.stdev_sam1)
            self.num_sam1 = self.num_sam1_edit.text()
            self.num_sam1 = int(self.num_sam1)
            
            self.mean_sam2 = self.mean_sam2_edit.text()
            self.mean_sam2 = float(self.mean_sam2)
            self.stdev_sam2 = self.std_sam2_edit.text()
            self.stdev_sam2 = float(self.stdev_sam2)
            self.num_sam2 = self.num_sam2_edit.text()
            self.num_sam2 = int(self.num_sam2)
            
        self.mean_sam1_label.setText("{:0.3f}".format(self.mean_sam1))
        self.mean_sam2_label.setText("{:0.3f}".format(self.mean_sam2))
        self.std_sam1_label.setText("{:0.3f}".format(self.stdev_sam1))
        self.std_sam2_label.setText("{:0.3f}".format(self.stdev_sam2))
        self.num_sam1_label.setText("{:0.0f}".format(self.num_sam1))
        self.num_sam2_label.setText("{:0.0f}".format(self.num_sam2))
            
    def calculation(self):
        sp = np.sqrt( ( (self.num_sam1-1)*self.stdev_sam1**2 + 
                        (self.num_sam2-1)*self.stdev_sam2**2 ) / 
                        (self.num_sam1+self.num_sam2-2) )
        stderr = sp * np.sqrt(1/self.num_sam1 + 1/self.num_sam2)
        t0, p = stats.ttest_ind_from_stats(self.mean_sam1, self.stdev_sam1, self.num_sam1,  
                                           self.mean_sam2, self.stdev_sam2, self.num_sam2,
                                           equal_var=True)   
        mean_dif = self.mean_sam1 - self.mean_sam2
        sig_lev = self.siglevel_edit.text()
        sig_lev = float(sig_lev)
        t_siglev = stats.t.ppf(1-sig_lev/2, self.num_sam1+self.num_sam2-2)
        conf_Int = stats.t.interval(1-sig_lev,self.num_sam1+self.num_sam2-2)
        lowerCI = self.mean_sam1 - self.mean_sam2 + conf_Int[0]*stderr
        upperCI = self.mean_sam1 - self.mean_sam2 + conf_Int[1]*stderr

        
        self.tsig_label.setText("{:0.3f}".format(t_siglev))         
        self.meandif_label.setText("{:0.3f}".format(mean_dif))        
        self.sp_label.setText("{:0.3f}".format(sp))
        self.stderr_label.setText("{:0.3f}".format(stderr))
        self.t0_label.setText("{:0.3f}".format(t0))
        self.p_label.setText("{:0.3f}".format(p))
        self.lowerCI_label.setText("{:0.3f}".format(lowerCI))
        self.upperCI_label.setText("{:0.3f}".format(upperCI))
        
        self.graph_canvas.plot_t(self.num_sam1+self.num_sam2-2,sig_lev,t0,t_siglev)
        
      
    
if __name__ == "__main__":
  
        app = QApplication(sys.argv)
        mw = window()
        mw.show()
        sys.exit(app.exec())