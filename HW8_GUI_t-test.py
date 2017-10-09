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
                            QMessageBox, QAbstractButton, QSlider, QLineEdit, QTabWidget)
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
        xmin = stats.t.ppf(0.0005,df)
        xmax = stats.t.ppf(0.9995,df)
        x = np.linspace(xmin,xmax, 100) #x = np.linspace(loc-3*scale,loc+3*scale, 100)
        y = stats.t.pdf(x,df)
        self.axes.set_xlabel("Student-t")
        self.axes.set_ylabel("PDF")
        self.axes.set_title("Two-Sided t-test for $\\alpha=%g$" %alpha)
        self.axes.plot(x,y,label='t distribution\nwith $\\nu=%g$' %df)
        arrowproperties = dict(width=2, headwidth=6, frac=0.2, facecolor='red',
                          shrink=0.1)
        if np.absolute(t0) < xmax:
            self.axes.plot(t0,0.0,'+',color='k',label='Test Statistic',markersize=18)
            self.axes.annotate('$t_0 = %0.3f $' %t0, xy=(t0,0), xytext=(t0,.1), xycoords='data', 
                               fontsize=10,arrowprops=arrowproperties)
        else:
            if t0 > 0:
                self.axes.annotate('$t_0 = %0.3f $' %t0, xy=(xmax-0.5,0.1), xytext=(xmax-3,0.1), 
                                   xycoords='data', fontsize=10,arrowprops=arrowproperties)
            else:
                self.axes.annotate('$t_0 = %0.3f $' %t0, xy=(xmin+0.5,0.1), xytext=(xmin+3,0.1), 
                                   xycoords='data', fontsize=10,arrowprops=arrowproperties)
                
        
        lowerFilledX = np.arange(xmin,-tsig,.01)
        lowerFilledY = stats.t.pdf(lowerFilledX, df)
        self.axes.fill_between(lowerFilledX,0,lowerFilledY, color='green' )
        upperFilledX = np.arange(tsig,xmax,.01)
        upperFilledY = stats.t.pdf(upperFilledX, df)
        self.axes.legend(loc=0,shadow=True)
        self.axes.fill_between(upperFilledX,0,upperFilledY, color='green' )
        self.axes.grid(True)        
        self.draw()
        
    def plot_normal_data(self,xs1,ys1,xfits1,yfits1,xs2,ys2,xfits2,yfits2):
        self.axes.clear()
        self.axes.set_xlabel("Sorted Data")
        self.axes.set_ylabel("Quantiles")
        self.axes.set_title("Normal Probability Plot")
        self.axes.plot(xs1,ys1,'ro',label='sample1')
        self.axes.plot(xs2,ys2,'go',label='sample2')
        self.axes.plot(xfits1,yfits1,label='best fit s1')
        self.axes.plot(xfits2,yfits2,label='best fit s2')
        self.axes.legend(loc=0,shadow=True)
        self.axes.grid(True)        
        self.draw() 
        
    def plot_normal_res(self,xs1,ys1,xfits1,yfits1,xs2,ys2,xfits2,yfits2,xlabel):
        self.axes.clear()
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel("Quantiles")
        self.axes.set_title("Normal Probability Plot")
        self.axes.plot(xs1,ys1,'ro',label='sample1')
        self.axes.plot(xfits1,yfits1,label='best fit s1')
        
        if xs2[3] != xs1[3]:
            self.axes.plot(xs2,ys2,'go',label='sample2')
            self.axes.plot(xfits2,yfits2,label='best fit s2')
        
        self.axes.legend(loc=0,shadow=True)
        self.axes.grid(True)        
        self.draw()    
        
    def plot_size(self,x,y):
        self.axes.clear()
        self.axes.set_xlabel("Sample Size")
        self.axes.set_ylabel("Length")
        self.axes.set_title("Sample size estimation")
        self.axes.plot(x,y)
        self.axes.legend(loc=0,shadow=True)
        self.axes.grid(True)        
        self.draw()   
        
    def plot_power(self,x,y,y_target,delta,nmin,alpha):
        self.axes.clear()
        self.axes.set_xlabel("Sample Size")
        self.axes.set_ylabel("Power")
        self.axes.set_title("Power Curves")
        self.axes.plot(x,y,label="$\\delta=%g$, $n_{min}=%g$" %(float("{:0.2f}".format(delta)),nmin))
        self.axes.plot(x,y_target,'r',label="$Target Power=%g$" %(1-alpha))
        self.axes.legend(loc=0,shadow=True)
        self.axes.grid(True)        
        self.draw()   
    
   
class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle('t-Test_Anvar Akhiiartdinov')
        
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
        
        #tab widget generation
        self.tab_widget = QTabWidget(self.main_widget)
        
        #tab1
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "t-test Plot")
        self.graph_canvas1 = MyDynamicMplCanvas(self.tab1, width=5, height=4, dpi=100)
        tab1_Layout = QVBoxLayout()
        tab1_Layout.addWidget(self.graph_canvas1)
        self.tab1.setLayout(tab1_Layout)
        
        #tab2
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, "Normal Probability Plot 1")
        self.graph_canvas2 = MyDynamicMplCanvas(self.tab2, width=5, height=4, dpi=100)
        tab2_Layout = QVBoxLayout()
        tab2_Layout.addWidget(self.graph_canvas2)
        self.tab2.setLayout(tab2_Layout)
        
        #tab3
        self.tab3 = QWidget()
        self.tab_widget.addTab(self.tab3, "Normal Probability Plot 2")
        self.graph_canvas3 = MyDynamicMplCanvas(self.tab3, width=5, height=4, dpi=100)
        tab3_Layout = QVBoxLayout()
        tab3_Layout.addWidget(self.graph_canvas3)
        self.tab3.setLayout(tab3_Layout)
        
        #tab4
        self.tab4 = QWidget()
        self.tab_widget.addTab(self.tab4, "Power Plot")
        self.graph_canvas4 = MyDynamicMplCanvas(self.tab4, width=5, height=4, dpi=100)
        
        self.slider1 = QSlider(self.tab4)
        self.slider1.setRange(5, 50)
        self.slider1.setValue(25)
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider1.setTickInterval(5)
        self.slider1.setOrientation(Qt.Horizontal)
        self.slider1.setGeometry(5, 5, 10, 10) 
        self.slider1.valueChanged.connect(self.calculation_same)
        self.slider1_label = QLabel("{:0.2f}".format(self.slider1.value()/100), self.tab4)      
        self.slider1_title = QLabel('Assumed Std Deviation', self.tab4)      
        
        self.slider2 = QSlider(self.tab4)
        self.slider2.setRange(20, 50)
        self.slider2.setValue(25)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        self.slider2.setTickInterval(5)
        self.slider2.setOrientation(Qt.Horizontal)
        self.slider2.setGeometry(5, 5, 10, 10) 
        self.slider2.valueChanged.connect(self.calculation_same)
        self.slider2_label = QLabel("{:0.2f}".format(self.slider2.value()/100), self.tab4)  
        self.slider2_title = QLabel('Critical Mean Difference', self.tab4)  
        
        slider1_layout = QHBoxLayout()
        slider1_layout.addWidget(self.slider1_label)
        slider1_layout.addWidget(self.slider1)
        slider2_layout = QHBoxLayout()
        slider2_layout.addWidget(self.slider2_label)
        slider2_layout.addWidget(self.slider2)
        tab4_Layout = QVBoxLayout()
        tab4_Layout.addWidget(self.graph_canvas4)
        tab4_Layout.addWidget(self.slider1_title)
        tab4_Layout.addLayout(slider1_layout)
        tab4_Layout.addWidget(self.slider2_title)
        tab4_Layout.addLayout(slider2_layout)
        self.tab4.setLayout(tab4_Layout)
        
        #tab5
        self.tab5 = QWidget()
        self.tab_widget.addTab(self.tab5, "Sample size")
        self.graph_canvas5 = MyDynamicMplCanvas(self.tab5, width=5, height=4, dpi=100)
        tab5_Layout = QVBoxLayout()
        tab5_Layout.addWidget(self.graph_canvas5)
        self.tab5.setLayout(tab5_Layout)
               
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
        self.mean_sam1_edit = QLineEdit("16.764",self.main_widget)
        self.mean_sam1_edit.setValidator(QDoubleValidator())
        self.mean_sam1_edit.setMaxLength(6)
        self.mean_sam1_edit.resize(10,20)
        self.mean_sam2_freeze_label = QLabel("Mean of Sample 2", self.main_widget)    
        self.mean_sam2_edit = QLineEdit("17.042",self.main_widget)
        self.mean_sam2_edit.setValidator(QDoubleValidator())
        self.mean_sam2_edit.setMaxLength(6)
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
        canvas_box_layout.addWidget(self.tab_widget)
        canvas_box.setLayout(canvas_box_layout)
        
        #Calculation area
        self.calc_button1 = QPushButton("Calculate: Variances Same", self.main_widget)
        self.calc_button1.clicked.connect(self.calculation_same)
        self.calc_button2 = QPushButton("Calculate: Variances Different", self.main_widget)
        self.calc_button2.clicked.connect(self.calculation_dif)
        self.calc_button3 = QPushButton("Calculate: Paired t-Test", self.main_widget)
        self.calc_button3.clicked.connect(self.calculation_pair)
        self.calc_button4 = QPushButton("Calculate: Known Sigmas", self.main_widget)
        self.calc_button4.clicked.connect(self.calculation_sigmas)
                     
        but_layout = QHBoxLayout()
        but_layout.addWidget(self.calc_button1)
        but_layout.addWidget(self.calc_button2)
        but_layout.addWidget(self.calc_button3)
        but_layout.addWidget(self.calc_button4)        
        
        self.siglevel_label_freeze = QLabel("Significance level", self.main_widget)
        self.siglevel_edit = QLineEdit("0.05",self.main_widget)
        self.siglevel_edit.setValidator(QDoubleValidator())
        self.siglevel_edit.setMaxLength(4)
        self.siglevel_edit.resize(10,20)
        
        sig_layout = QHBoxLayout()
        sig_layout.addWidget(self.siglevel_label_freeze)
        sig_layout.addWidget(self.siglevel_edit)
        
        self.dof_label_freeze = QLabel("DOF", self.main_widget)
        self.dof_label = QLabel("Not calculated", self.main_widget)
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
        calc_freeze_layout.addWidget(self.dof_label_freeze) 
        calc_freeze_layout.addWidget(self.meandif_label_freeze)
        calc_freeze_layout.addWidget(self.sp_label_freeze)
        calc_freeze_layout.addWidget(self.stderr_label_freeze)
        calc_freeze_layout.addWidget(self.tsig_label_freeze)
        calc_freeze_layout.addWidget(self.t0_label_freeze)
        calc_freeze_layout.addWidget(self.p_label_freeze)
        calc_freeze_layout.addWidget(self.lowerCI_label_freeze)
        calc_freeze_layout.addWidget(self.upperCI_label_freeze)
        
        calc_layout = QVBoxLayout()
        calc_layout.addWidget(self.dof_label)
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
        ver_layout.addLayout(but_layout)
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
    '''
    def valuechange(self):
        self.sigma = self.slider1.value()/100
        self.slider1_label.setText("{:0.2f}".format(self.sigma))
    ''' 
    
    def compute_stats(self):
        
        if self.table_checkbox.isChecked():
            sample1_list=[]
            sample2_list=[]
            for row in range(self.data_table.rowCount()):
                sample1_list.append(float(self.data_table.item(row,1).text()))
                sample2_list.append(float(self.data_table.item(row,2).text()))
            
            self.sam1_array = np.asarray(sample1_list)
            self.mean_sam1 = np.mean(self.sam1_array)
            self.stdev_sam1 = np.std(self.sam1_array,ddof=1)
            self.num_sam1 = len(self.sam1_array)
            
            self.sam2_array = np.asarray(sample2_list)
            self.mean_sam2 = np.mean(self.sam2_array)
            self.stdev_sam2 = np.std(self.sam2_array,ddof=1)
            self.num_sam2 = len(self.sam2_array)
            
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
            
    def calculation_same(self):
        #mean_cr,ok = QInputDialog.getDouble(self,"Float input dualog","enter critical difference in mean",decimals=4)
        mean_cr = self.slider2.value()/100
        self.slider2_label.setText("{:0.3f}".format(mean_cr))
        
        sigma = self.slider1.value()/100
        self.slider1_label.setText("{:0.3f}".format(sigma))
        
        dof = self.num_sam1 + self.num_sam2 - 2
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
        print(conf_Int)
        p_check = stats.t.sf(np.absolute(t0),dof)
        print("Pcheck=",p_check)
                
        delta = mean_cr / sigma
        sam_size = np.arange(2,30,1)
        y_axis = np.zeros(len(sam_size))
        for i in range(len(sam_size)):
            y_axis[i] = t_siglev * np.sqrt(2/sam_size[i])    
        self.graph_canvas5.plot_size(sam_size,y_axis)
                
        power = np.zeros(len(sam_size))
        for i in sam_size:
            adj = delta / np.sqrt(2/i)
            df = 2*i-2
            cilow = stats.t.ppf(sig_lev/2,df)
            cihig = stats.t.ppf(1-sig_lev/2,df)
            power[i-2] = 1 - stats.t.cdf(cihig-adj,df) + stats.t.cdf(cilow-adj,df)
            
        min_sam_size = sam_size[np.sum(np.less(power,1-sig_lev))] 
        actual_power = power[np.sum(np.less(power,1-sig_lev))] 
        
        self.graph_canvas4.plot_power(sam_size,power,1-sig_lev*np.ones(len(sam_size)),
                                          delta,min_sam_size,sig_lev)
        
        self.dof_label.setText("{:0.0f}".format(dof))      
        self.tsig_label.setText("{:0.3f}".format(t_siglev))         
        self.meandif_label.setText("{:0.4f}".format(mean_dif))        
        self.sp_label.setText("{:0.3f}".format(sp))
        self.stderr_label.setText("{:0.3f}".format(stderr))
        self.t0_label.setText("{:0.3f}".format(t0))
        self.p_label.setText("{:0.3f}".format(p))
        self.lowerCI_label.setText("{:0.4f}".format(lowerCI))
        self.upperCI_label.setText("{:0.4f}".format(upperCI))
                       
        self.graph_canvas1.plot_t(self.num_sam1+self.num_sam2-2,sig_lev,t0,t_siglev)
        
        if self.table_checkbox.isChecked():
            res_s1 = stats.probplot(self.sam1_array, dist='norm', fit=False, plot=None)
            coeffs_s1 = np.polyfit(res_s1[1], res_s1[0], 1)
            minx_s1 = np.min(res_s1[1])
            maxx_s1 = np.max(res_s1[1])
            xfit_s1 = np.array([minx_s1,maxx_s1])
            yfit_s1 = coeffs_s1[1] + xfit_s1*coeffs_s1[0]
            
            res_s2 = stats.probplot(self.sam2_array, dist='norm', fit=False, plot=None)
            coeffs_s2 = np.polyfit(res_s2[1], res_s2[0], 1)
            minx_s2 = np.min(res_s2[1])
            maxx_s2 = np.max(res_s2[1])
            xfit_s2 = np.array([minx_s2,maxx_s2])
            yfit_s2 = coeffs_s2[1] + xfit_s2*coeffs_s2[0]
            
            self.graph_canvas2.plot_normal_data(res_s1[1],res_s1[0],xfit_s1,yfit_s1,
                                                res_s2[1],res_s2[0],xfit_s2,yfit_s2)
            
            res_s1 = stats.probplot(self.sam1_array-self.mean_sam1, dist='norm', fit=False, plot=None)
            coeffs_s1 = np.polyfit(res_s1[1], res_s1[0], 1)
            minx_s1 = np.min(res_s1[1])
            maxx_s1 = np.max(res_s1[1])
            xfit_s1 = np.array([minx_s1,maxx_s1])
            yfit_s1 = coeffs_s1[1] + xfit_s1*coeffs_s1[0]
            
            res_s2 = stats.probplot(self.sam2_array-self.mean_sam2, dist='norm', fit=False, plot=None)
            coeffs_s2 = np.polyfit(res_s2[1], res_s2[0], 1)
            minx_s2 = np.min(res_s2[1])
            maxx_s2 = np.max(res_s2[1])
            xfit_s2 = np.array([minx_s2,maxx_s2])
            yfit_s2 = coeffs_s2[1] + xfit_s2*coeffs_s2[0]
            
            self.graph_canvas3.plot_normal_res(res_s1[1],res_s1[0],xfit_s1,yfit_s1,
                                               res_s2[1],res_s2[0],xfit_s2,yfit_s2,"Sorted Residuals")
    
        
    def calculation_dif(self):
        t0, p = stats.ttest_ind_from_stats(self.mean_sam1, self.stdev_sam1, self.num_sam1,  
                                           self.mean_sam2, self.stdev_sam2, self.num_sam2,
                                           equal_var=False)   
        print(p)
        mean_dif = self.mean_sam1 - self.mean_sam2
        dof = (self.stdev_sam1**2/self.num_sam1 + self.stdev_sam2**2/self.num_sam2)**2 / \
              ( (self.stdev_sam1**2/self.num_sam1)**2/(self.num_sam1-1) + \
                (self.stdev_sam2**2/self.num_sam2)**2/(self.num_sam2-1) )
        dof = np.round_(dof)
        stderr = np.sqrt(self.stdev_sam1**2/self.num_sam1 + self.stdev_sam2**2/self.num_sam2)
        sig_lev = self.siglevel_edit.text()
        sig_lev = float(sig_lev)
        t_siglev = stats.t.ppf(1-sig_lev/2, dof)
        conf_Int = stats.t.interval(1-sig_lev,dof)
        lowerCI = self.mean_sam1 - self.mean_sam2 + conf_Int[0]*stderr
        upperCI = self.mean_sam1 - self.mean_sam2 + conf_Int[1]*stderr
        
        self.dof_label.setText("{:0.0f}".format(dof))      
        self.tsig_label.setText("{:0.3f}".format(t_siglev))         
        self.meandif_label.setText("{:0.4f}".format(mean_dif))        
        self.sp_label.setText("Variances are different")
        self.stderr_label.setText("{:0.3f}".format(stderr))
        self.t0_label.setText("{:0.3f}".format(t0))
        self.p_label.setText("{:0.5f}".format(p))
        self.lowerCI_label.setText("{:0.4f}".format(lowerCI))
        self.upperCI_label.setText("{:0.4f}".format(upperCI))                      
      
        self.graph_canvas1.plot_t(dof,sig_lev,t0,t_siglev)
        
        if self.table_checkbox.isChecked():
            res_s1 = stats.probplot(self.sam1_array, dist='norm', fit=False, plot=None)
            coeffs_s1 = np.polyfit(res_s1[1], res_s1[0], 1)
            minx_s1 = np.min(res_s1[1])
            maxx_s1 = np.max(res_s1[1])
            xfit_s1 = np.array([minx_s1,maxx_s1])
            yfit_s1 = coeffs_s1[1] + xfit_s1*coeffs_s1[0]
            
            res_s2 = stats.probplot(self.sam2_array, dist='norm', fit=False, plot=None)
            coeffs_s2 = np.polyfit(res_s2[1], res_s2[0], 1)
            minx_s2 = np.min(res_s2[1])
            maxx_s2 = np.max(res_s2[1])
            xfit_s2 = np.array([minx_s2,maxx_s2])
            yfit_s2 = coeffs_s2[1] + xfit_s2*coeffs_s2[0]
            
            self.graph_canvas2.plot_normal_data(res_s1[1],res_s1[0],xfit_s1,yfit_s1,
                                                res_s2[1],res_s2[0],xfit_s2,yfit_s2)
            
            res_s1 = stats.probplot(self.sam1_array-self.mean_sam1, dist='norm', fit=False, plot=None)
            coeffs_s1 = np.polyfit(res_s1[1], res_s1[0], 1)
            minx_s1 = np.min(res_s1[1])
            maxx_s1 = np.max(res_s1[1])
            xfit_s1 = np.array([minx_s1,maxx_s1])
            yfit_s1 = coeffs_s1[1] + xfit_s1*coeffs_s1[0]
            
            res_s2 = stats.probplot(self.sam2_array-self.mean_sam2, dist='norm', fit=False, plot=None)
            coeffs_s2 = np.polyfit(res_s2[1], res_s2[0], 1)
            minx_s2 = np.min(res_s2[1])
            maxx_s2 = np.max(res_s2[1])
            xfit_s2 = np.array([minx_s2,maxx_s2])
            yfit_s2 = coeffs_s2[1] + xfit_s2*coeffs_s2[0]
            
            self.graph_canvas3.plot_normal_res(res_s1[1],res_s1[0],xfit_s1,yfit_s1,
                                               res_s2[1],res_s2[0],xfit_s2,yfit_s2,"Sorted Residuals")
            
    def calculation_pair(self):
        diff = self.sam1_array - self.sam2_array
        mean_diff = np.mean(diff)
        stdev_diff = np.std(diff,ddof=1)
        stderr = stdev_diff/np.sqrt(self.num_sam1)
        
        sig_lev = self.siglevel_edit.text()
        sig_lev = float(sig_lev)
        dof = self.num_sam1 - 1
        t_siglev = stats.t.ppf(1-sig_lev/2, dof)
        t0 = mean_diff / stdev_diff * np.sqrt(self.num_sam1)
        conf_Int = stats.t.interval(1-sig_lev,dof)
        lowerCI = mean_diff + conf_Int[0]*stderr
        upperCI = mean_diff + conf_Int[1]*stderr
        p = stats.t.sf(np.abs(t0), dof)*2
                
        self.dof_label.setText("{:0.0f}".format(dof))      
        self.tsig_label.setText("{:0.3f}".format(t_siglev))         
        self.meandif_label.setText("{:0.4f}".format(mean_diff))        
        self.sp_label.setText("{:0.4f}".format(stdev_diff**2))
        self.stderr_label.setText("{:0.4f}".format(stderr))
        self.t0_label.setText("{:0.3f}".format(t0))
        self.p_label.setText("{:0.3f}".format(p))
        self.lowerCI_label.setText("{:0.4f}".format(lowerCI))
        self.upperCI_label.setText("{:0.4f}".format(upperCI))     
        
        self.graph_canvas1.plot_t(dof,sig_lev,t0,t_siglev)
        
        if self.table_checkbox.isChecked():
            res_s1 = stats.probplot(self.sam1_array, dist='norm', fit=False, plot=None)
            coeffs_s1 = np.polyfit(res_s1[1], res_s1[0], 1)
            minx_s1 = np.min(res_s1[1])
            maxx_s1 = np.max(res_s1[1])
            xfit_s1 = np.array([minx_s1,maxx_s1])
            yfit_s1 = coeffs_s1[1] + xfit_s1*coeffs_s1[0]
            
            res_s2 = stats.probplot(self.sam2_array, dist='norm', fit=False, plot=None)
            coeffs_s2 = np.polyfit(res_s2[1], res_s2[0], 1)
            minx_s2 = np.min(res_s2[1])
            maxx_s2 = np.max(res_s2[1])
            xfit_s2 = np.array([minx_s2,maxx_s2])
            yfit_s2 = coeffs_s2[1] + xfit_s2*coeffs_s2[0]
            
            self.graph_canvas2.plot_normal_data(res_s1[1],res_s1[0],xfit_s1,yfit_s1,
                                                res_s2[1],res_s2[0],xfit_s2,yfit_s2)
            
            
            ratios = self.sam1_array / self.sam2_array
            res_r = stats.probplot(ratios, dist='norm', fit=False, plot=None)
            coeffs_r = np.polyfit(res_r[1], res_r[0], 1)
            minx_r = np.min(res_r[1])
            maxx_r = np.max(res_r[1])
            xfit_r = np.array([minx_r,maxx_r])
            yfit_r = coeffs_r[1] + xfit_r*coeffs_r[0]
            
            self.graph_canvas3.plot_normal_res(res_r[1],res_r[0],xfit_r,yfit_r,
                                               res_r[1],res_r[0],xfit_r,yfit_r,"Sorted Ratios")
        
    def calculation_sigmas(self):
            
        sigma1,ok = QInputDialog.getDouble(self,"Float input dualog","enter a number",decimals=4)
        sigma2,ok = QInputDialog.getDouble(self,"Float input dualog","enter a number",decimals=4)
        stderr = np.sqrt(sigma1**2/self.num_sam1 + sigma2**2/self.num_sam2)
        mean_dif = self.mean_sam1 - self.mean_sam2
        t0 = mean_dif/stderr
        p = stats.norm.sf(t0)*2
        sig_lev = self.siglevel_edit.text()
        sig_lev = float(sig_lev)
        t_siglev = stats.norm.ppf(1-sig_lev/2)
        conf_Int = stats.norm.interval(1-sig_lev)
        print(t_siglev)
        print(conf_Int)
        lowerCI = self.mean_sam1 - self.mean_sam2 + conf_Int[0]*stderr
        upperCI = self.mean_sam1 - self.mean_sam2 + conf_Int[1]*stderr
        
        self.dof_label.setText("Known sigmas")      
        self.tsig_label.setText("{:0.3f}".format(t_siglev))         
        self.meandif_label.setText("{:0.4f}".format(mean_dif))        
        self.sp_label.setText("Known Sigmas")
        self.stderr_label.setText("{:0.3f}".format(stderr))
        self.t0_label.setText("{:0.3f}".format(t0))
        self.p_label.setText("{:0.3f}".format(p))
        self.lowerCI_label.setText("{:0.4f}".format(lowerCI))
        self.upperCI_label.setText("{:0.4f}".format(upperCI))
                       
        self.graph_canvas1.plot_t(1000,sig_lev,t0,t_siglev)
        
        if self.table_checkbox.isChecked():
            res_s1 = stats.probplot(self.sam1_array, dist='norm', fit=False, plot=None)
            coeffs_s1 = np.polyfit(res_s1[1], res_s1[0], 1)
            minx_s1 = np.min(res_s1[1])
            maxx_s1 = np.max(res_s1[1])
            xfit_s1 = np.array([minx_s1,maxx_s1])
            yfit_s1 = coeffs_s1[1] + xfit_s1*coeffs_s1[0]
            
            res_s2 = stats.probplot(self.sam2_array, dist='norm', fit=False, plot=None)
            coeffs_s2 = np.polyfit(res_s2[1], res_s2[0], 1)
            minx_s2 = np.min(res_s2[1])
            maxx_s2 = np.max(res_s2[1])
            xfit_s2 = np.array([minx_s2,maxx_s2])
            yfit_s2 = coeffs_s2[1] + xfit_s2*coeffs_s2[0]
            
            self.graph_canvas2.plot_normal_data(res_s1[1],res_s1[0],xfit_s1,yfit_s1,
                                                res_s2[1],res_s2[0],xfit_s2,yfit_s2)
            
            res_s1 = stats.probplot(self.sam1_array-self.mean_sam1, dist='norm', fit=False, plot=None)
            coeffs_s1 = np.polyfit(res_s1[1], res_s1[0], 1)
            minx_s1 = np.min(res_s1[1])
            maxx_s1 = np.max(res_s1[1])
            xfit_s1 = np.array([minx_s1,maxx_s1])
            yfit_s1 = coeffs_s1[1] + xfit_s1*coeffs_s1[0]
            
            res_s2 = stats.probplot(self.sam2_array-self.mean_sam2, dist='norm', fit=False, plot=None)
            coeffs_s2 = np.polyfit(res_s2[1], res_s2[0], 1)
            minx_s2 = np.min(res_s2[1])
            maxx_s2 = np.max(res_s2[1])
            xfit_s2 = np.array([minx_s2,maxx_s2])
            yfit_s2 = coeffs_s2[1] + xfit_s2*coeffs_s2[0]
            
            self.graph_canvas3.plot_normal_res(res_s1[1],res_s1[0],xfit_s1,yfit_s1,
                                               res_s2[1],res_s2[0],xfit_s2,yfit_s2,"Sorted Residuals")
  
        
    
if __name__ == "__main__":
  
        app = QApplication(sys.argv)
        mw = window()
        mw.show()
        sys.exit(app.exec())