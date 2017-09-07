# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 10:40:44 2017

@author: cwv414
"""

#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem,QSizePolicy,
                             QGridLayout,QGroupBox, QMainWindow, QInputDialog)
from PyQt5.QtWidgets import QAction, qApp

from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QIcon

import numpy as np

from scipy import stats


import os
 
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.mlab as mlab

global data_labelx, data_labely, bin_count

data_labelx="Temp"
data_labely="Prob"
bin_count=50

rcParams.update({'figure.autolayout': True})

class StatsMainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):               
        
        
        
        center=StatsCalculator()
        
        OpenAct = QAction('&Open', self)        
        OpenAct.setShortcut('Ctrl+O')
        OpenAct.setStatusTip('Open File')
        OpenAct.triggered.connect(center.load_data)
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(OpenAct)
           
        
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Chris Vasquez HW2 Stats Calculator')    
        self.show()
        
        self.setCentralWidget(center)
        



class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
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
        filename = "ExportedGraph.pdf"
        self.fig.savefig(filename)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Saved a copy of the graphics window to {}".format(filename))
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Saved PDF File")
        msg.setDetailedText("The full path of the file is \n{}".format(os.path.abspath(os.getcwd())))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowModality(Qt.ApplicationModal)
        msg.exec_()
        print("Exported PDF file")
        
class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself frequently with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.axes.set_xlabel("X Label")
        self.axes.set_ylabel("Y Label")
        self.axes.set_title("Title")
             
    def plot_histogram(self,data_array):
        global data_labelx, data_labely, bin_count
        self.axes.cla() #Clear axes
        self.axes.hist(data_array,bins=bin_count,
                       normed=True,label="Emperical",
                       edgecolor='b',color='y')
        self.axes.set_xlabel(data_labelx)
        self.axes.set_ylabel(data_labely)
        self.axes.set_title("Normalized Probability Plot")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Normalized Histogram.")
          
    def plot_normal(self,mu,sigma):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(mu-3*sigma,mu+3*sigma, 100)
        y = mlab.normpdf(x, mu, sigma)
        self.axes.plot(x,y,label="Normal")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Normal Distribution.")
        
    def plot_hypsec(self,apara,bpara):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(apara-5*bpara,apara+5*bpara, 100)
        y = stats.hypsecant.pdf(x,apara,bpara)
        self.axes.plot(x,y,label="Hyperbolic Secant")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Hyperbolic Secant Distribution.")
        
    def plot_gamma(self,agam,bgam,cgam):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace((bgam+agam*cgam)-3*(cgam*cgam*agam)**0.5,(bgam+agam*cgam)+3*(cgam*cgam*agam)**0.5, 100)
        y = stats.gamma.pdf(x,agam,bgam,cgam)
        self.axes.plot(x,y,label="Gamma")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Gamma Distribution.")
        
    def plot_chi2(self,chi2a,chi2b,chi2c,meanval,stdval):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(meanval-3*stdval,meanval+3*stdval, 100)
        y = stats.chi2.pdf(x,chi2a,chi2b,chi2c)
        self.axes.plot(x,y,label="Chi Squard")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Chi Squared Distribution.")
        
    def plot_beta(self,betaa,betab,betac,betad,meanval,stdval):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(meanval-3.5*stdval,meanval+3.5*stdval, 100)
        y = stats.beta.pdf(x,betaa,betab,betac,betad)
        self.axes.plot(x,y,label="Beta")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Beta Distribution.")
        
        
class StatsCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              
    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,1000,500)

        self.load_button = QPushButton('Load Data',self)
        self.load_button.clicked.connect(self.load_data)

        self.xaxis_label=QPushButton('Set X-Axis Label',self)
        self.xaxis_label.clicked.connect(self.xaxis_fnc)

        self.yaxis_label=QPushButton('Set Y-Axis Label',self)
        self.yaxis_label.clicked.connect(self.yaxis_fnc)

        self.slider=QSlider(Qt.Horizontal,self)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setGeometry(30,40,100,300)
        self.slider.valueChanged[int].connect(self.slider_val)




     
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.std_label = QLabel("Std Dev: Not Computed Yet",self)
        self.median_label = QLabel("Median: Not Computed Yet", self)
        self.var_label = QLabel("Variance: Not Computed Yet", self)
        self.range_label = QLabel("Range: Not Computed Yet", self)
        self.min_label = QLabel("Min: Not Computed Yet", self)
        self.max_label = QLabel("Max: Not Computed Yet", self)
        self.sum_label = QLabel("Sum: Not Computed Yet", self)
        self.stderr_label=QLabel("Std Error: Not Computed Yet", self)
        self.kurt_label=QLabel("Kurtosis: Not Computed Yet", self)
        self.skew_label=QLabel("Skew: Not Computed Yet", self)
        self.count_label=QLabel("Count: Not Computed Yet", self)
        self.mode_label=QLabel("Mode: Not Computed Yet", self)
        
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        self.main_widget = QWidget(self)
        self.graph_canvas = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)

        
        #Define where the widgets go in the window
        #We start by defining some boxes that we can arrange
        
        #Create a GUI box to put all the table and data widgets in
        table_box = QGroupBox("Data Table")
        #Create a layout for that box using the vertical
        table_box_layout = QVBoxLayout()
        #Add the widgets into the layout
        table_box_layout.addWidget(self.load_button)
        table_box_layout.addWidget(self.data_table)
        #setup the layout to be displayed in the box
        table_box.setLayout(table_box_layout)
        
        #repeat the box layout for Statistics
        stats_box = QGroupBox("Summary Statistics")
        stats_box_layout = QVBoxLayout()
        stats_box_layout.addWidget(self.mean_label)
        stats_box_layout.addWidget(self.stderr_label)
        stats_box_layout.addWidget(self.median_label)
        stats_box_layout.addWidget(self.mode_label)
        stats_box_layout.addWidget(self.std_label)
        stats_box_layout.addWidget(self.var_label)
        stats_box_layout.addWidget(self.kurt_label)
        stats_box_layout.addWidget(self.skew_label)
        stats_box_layout.addWidget(self.range_label)
        stats_box_layout.addWidget(self.min_label)
        stats_box_layout.addWidget(self.max_label)
        stats_box_layout.addWidget(self.sum_label)
        stats_box_layout.addWidget(self.count_label)
        
        stats_box.setLayout(stats_box_layout)

        #Ignore the box creation for now, since the graph box would just have 1 widget
        #graph_box = QGroupBox("Data and Probability Graph")
        
        #Create some distribution options
        #Start with creating a check button.
        self.normal_checkbox = QCheckBox('Normal Distribution',self)
        self.normal_checkbox.stateChanged.connect(self.compute_stats)
        
        self.hyp_sec_checkbox=QCheckBox('Hyperbolic Secant Distribution',self)
        self.hyp_sec_checkbox.stateChanged.connect(self.compute_stats)
        
        self.gamma_checkbox=QCheckBox('Gamma Distribution',self)
        self.gamma_checkbox.stateChanged.connect(self.compute_stats)
        
        self.chi2_checkbox=QCheckBox('Chi Squard Distribution',self)
        self.chi2_checkbox.stateChanged.connect(self.compute_stats)
        
        self.beta_checkbox=QCheckBox('Beta Distribution',self)
        self.beta_checkbox.stateChanged.connect(self.compute_stats)
        
        
        
        distribution_box = QGroupBox("Distribution Functions")
        distribution_box_layout= QVBoxLayout()
        distribution_box_layout.addWidget(self.normal_checkbox)
        distribution_box_layout.addWidget(self.hyp_sec_checkbox)
        distribution_box_layout.addWidget(self.gamma_checkbox)
        distribution_box_layout.addWidget(self.chi2_checkbox)
        distribution_box_layout.addWidget(self.beta_checkbox)
        distribution_box.setLayout(distribution_box_layout)

        label_box=QGroupBox("")
        label_box_layout=QVBoxLayout()
        label_box_layout.addWidget(self.xaxis_label)
        label_box_layout.addWidget(self.yaxis_label)
        label_box.setLayout(label_box_layout)

        graph_box = QGroupBox("Data and Probability Graph")
        graph_box_layout=QVBoxLayout()
        graph_box_layout.addWidget(self.graph_canvas)
        graph_box_layout.addWidget(self.slider)
        graph_box.setLayout(graph_box_layout)
        
        #Now we can set all the previously defined boxes into the main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(graph_box,0,1) 
        grid_layout.addWidget(distribution_box,1,1)
        grid_layout.addWidget(label_box,0,2)
        
        self.setLayout(grid_layout)
        
        self.setWindowTitle('Introduction to Descriptive Statistics - Chris Vasquez')
        self.activateWindow()
        self.raise_()
        self.show()
    
    def xaxis_fnc(self):
        global data_labelx
        d_labelx, submit=QInputDialog.getText(self,'Input Dialog','X-Axis Label')
        if submit:
            data_labelx=d_labelx
            self.compute_stats()
            
    def yaxis_fnc(self):
        global data_labely
        d_labely, submit=QInputDialog.getText(self,'Input Dialog','Y-Axis Label')
        if submit:
            data_labely=d_labely
            self.compute_stats()

    def slider_val(self, value):
        global bin_count
        if value > 0:
            print(value)
            bin_count=value
            self.compute_stats()



    def load_data(self):        
       #for this example, we'll hard code the file name.
       options=QFileDialog.Options()
       options|=QFileDialog.DontUseNativeDialog
       data_file_name, _ = QFileDialog.getOpenFileName(self,"Select CSV File", "", "All Files (*);;CSV Files (*.csv)", options=options)
       header_row = 1 
       #load data file into memory as a list of lines       
       with open(data_file_name,'r') as data_file:
            self.data_lines = data_file.readlines()
        
       print("Opened {}".format(data_file_name))
       print(self.data_lines[1:10]) #for debugging only
        
       #Set the headers
       #parse the lines by stripping the newline character off the end
       #and then splitting them on commas.
       data_table_columns = self.data_lines[header_row].strip().split(',')
       self.data_table.setColumnCount(len(data_table_columns))
       self.data_table.setHorizontalHeaderLabels(data_table_columns)
        
       #fill the table starting with the row after the header
       current_row = -1
       for row in range(header_row+1, len(self.data_lines)):
           row_values = (self.data_lines[row].strip().split(','))
           current_row +=1
           self.data_table.insertRow(current_row)
           #Populate the row with data
           for col in range(len(data_table_columns)):
               entry = QTableWidgetItem("{}".format(row_values[col]))
               self.data_table.setItem(current_row,col,entry)
       print("Filled {} rows.".format(row))
    
    def compute_stats(self):
        
        #setup array
        item_list=[]
        items = self.data_table.selectedItems()
        for item in items:
            try:
                item_list.append(float(item.text()))
            except:
                pass
        
        if len(item_list) > 1: #Check to see if there are 2 or more samples
            data_array = np.asarray(item_list)
            mean_value = np.mean(data_array)
            stdev_value = np.std(data_array)
            median_value=np.median(data_array)
            var_value=np.var(data_array)
            range_value=np.ptp(data_array)
            min_value=np.amin(data_array)
            max_value=np.amax(data_array)
            sum_value=np.sum(data_array)
            stderr_value=stats.sem(data_array)
            kurt_value=stats.kurtosis(data_array)
            skew_value=stats.skew(data_array)
            count_value=sum_value/mean_value
            mode_array=stats.mode(data_array)
            mode_array2=np.array(mode_array)
            mode_value=mode_array2[0]
            
            #hyperbolic secant values
            bpara_value=stdev_value*2/3.14159
            
            print("Mean = {0:5f}".format(mean_value))
            
            
            self.mean_label.setText("Mean = {:0.4f}".format(mean_value))
            self.std_label.setText("Std Dev = {:0.4f}".format(stdev_value))
            self.median_label.setText("Median = {:0.4f}".format(median_value))
            self.var_label.setText("Variance = {:0.4f}".format(var_value))
            self.range_label.setText("Range = {:0.4f}".format(range_value))
            self.min_label.setText("Min = {:0.4f}".format(min_value))
            self.max_label.setText("Max = {:0.4f}".format(max_value))
            self.sum_label.setText("Sum = {:0.4f}".format(sum_value))
            self.stderr_label.setText("Std Error = {:0.4f}".format(stderr_value))
            self.kurt_label.setText("Kurtosis = {:0.4f}".format(kurt_value))
            self.skew_label.setText("Skew = {:0.4f}".format(skew_value))
            self.count_label.setText("Count = {:0.4f}".format(count_value))
            self.mode_label.setText("Mode = {:0.4f}".format(mode_value[0]))
            
            self.graph_canvas.plot_histogram(data_array)
            
            
            
            if self.normal_checkbox.isChecked():
                self.graph_canvas.plot_normal(mean_value,stdev_value)
                
            if self.hyp_sec_checkbox.isChecked():                
                self.graph_canvas.plot_hypsec(mean_value,bpara_value)
                
            if self.gamma_checkbox.isChecked():
                gam_value=stats.gamma.fit(data_array)
                self.graph_canvas.plot_gamma(gam_value[0],gam_value[1],gam_value[2])
            
            if self.chi2_checkbox.isChecked():
                chi2_value=stats.chi2.fit(data_array)
                self.graph_canvas.plot_chi2(chi2_value[0],chi2_value[1],chi2_value[2],mean_value,stdev_value)
            
            if self.beta_checkbox.isChecked():
                beta_value=stats.beta.fit(data_array)
                self.graph_canvas.plot_beta(beta_value[0],beta_value[1],beta_value[2],beta_value[3],mean_value,stdev_value)
           
            
        
'''       
  1. Add the ability to plot a normalized Histogram of the selected data in the table.
  2. Add a menu option to open a CSV data file.
  3. Add a checkbox for at least 5 distribution functions to plot over the top of the Histogram. 
    a. Include a legend and appropriate labels on your graph.
    b. Include axes labels. (Challenge: make the labels editable in your program).
  4. Use a grid style layout for your GUI
  5. Save the plot to a PDF when you double click on it.
  6. Try to find one of the most obscure distributions as one of your 5. Please try to be different than everyone else. 
  7. Print and turn in a screenshot of your GUI on one page. Be sure your name in in the window title.
  8. Print and turn in the PDF file of the properly labeled Histogram with 2 distributions shown.
'''

if __name__ == '__main__':
    #Start the program this way according to https://stackoverflow.com/questions/40094086/python-kernel-dies-for-second-run-of-pyqt5-gui
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    execute = StatsMainWindow()
    sys.exit(app.exec_())
