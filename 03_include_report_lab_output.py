#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem,QSizePolicy,
                             QGridLayout,QGroupBox)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
import numpy as np
from scipy import stats
import statistics
import math
#import collections
import PyQt5

import os
 
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.mlab as mlab

rcParams.update({'figure.autolayout': True})

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
             
    def plot_histogram(self,data_array,bins):
        data_label="Temperature"
        title="Probability Density Function Plots"
        self.axes.cla() #Clear axes
        self.axes.hist(data_array,bins=bins,
                       normed=True,label="Emperical",
                       edgecolor='b',color='y')
        self.axes.set_xlabel(data_label)
        self.axes.set_ylabel("Estimated Prob. Density Funct.")
        self.axes.set_title(title)
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
        
    def plot_contin(self, maxval, minval):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(minval,maxval, 100)
        y=[]
        for i in range(100):
            y.append(1/(maxval-minval))
        #y=sumvals/(maxval-minval)
        self.axes.plot(x,y,label="Uniform")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Uniform Distribution.")
        
    def plot_triang(self, maxval, minval, modeval):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(minval,maxval, math.floor(maxval-minval))
        y=[]
        for i in range(math.floor(minval), math.floor(modeval)):
            y.append(2*(i-minval)/(maxval-minval)/(modeval-minval))
        for i in range(math.floor(modeval), math.floor(maxval)):
            y.append(2*(maxval-i)/(maxval-minval)/(maxval-modeval))
        #y=sumvals/(maxval-minval)
        self.axes.plot(x,y,label="Triangular")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Triangular Distribution.")
        
    def plot_quad(self, maxval, minval):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(minval,maxval, math.floor(maxval-minval))
        y=[]
        alpha=12/(maxval-minval)**3
        beta=(maxval+minval)/2
        spread=math.floor(maxval)-math.floor(minval)
        for i in range(0,spread):
            y.append(alpha*((i+minval)-beta)**2)
        self.axes.plot(x,y,label="U-Quadratic")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing U-Quadratic Distribution.")
        
    def plot_log(self,m,sd):
        xmin,xmax = self.axes.get_xlim()
        
        v=sd**2
        mu=np.log(m/(1+v/m**2)**0.5)
        sigma=(np.log(1+v/m**2))**0.5
        x = np.linspace(m-3*sd,m+3*sd, 100)
        self.axes.plot(x,self.log_plot(x, mu, sigma),label="Log-Normal")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Log-Normal Distribution.")
    def log_plot(self, value, mu, sigma):
        coef=1/value/sigma/(2*math.pi)**0.5
        expon=-1*(((np.log(value))-mu)**2)/(2*sigma**2)
        calcedVal=coef*np.exp(expon)
        #print('{0} {1} {2}'.format(coef, expon, calcedVal)) 
        return calcedVal
        
class StatCalculator(QtWidgets.QMainWindow):#(QWidget):
    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              
    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,1000,800)
        main_widget=QWidget()
        #majorWidget=QWidget()
        self.setCentralWidget(main_widget)#(majorWidget)
        
        openFile = QtWidgets.QAction(QIcon('Open-icon.png'),'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openingFile)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        self.setWindowTitle('Introduction to Descriptive Statistics - Austin V')
        self.activateWindow()
        self.raise_()
        self.show()

        #super().__init__()#super(StatCalculator, self).__init__(self)
        self.load_button = QPushButton('Load Data',self)
        self.load_button.clicked.connect(self.simpLoad)
     
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.median_label = QLabel("Median: Not Computed Yet",self)
        self.mode_label=QLabel("Mode: Not Computed Yet", self)
        self.stdDev_label = QLabel("Standard Deviation: Not Computed Yet",self)
        self.kurt_label=QLabel("Kurtosis: Not Computed Yet",self)
        self.skew_label=QLabel("Skew: Not Computed Yet",self)
        self.minVal_label=QLabel("Minimum: Not Computed Yet",self)
        self.maxVal_label=QLabel("Maximum: Not Computed Yet",self)
        self.range_label = QLabel("Range: Not Computed Yet",self)
        self.sumT_label=QLabel("Sum: Not Computed Yet",self)
        
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
        stats_box_layout.addWidget(self.median_label)
        stats_box_layout.addWidget(self.mode_label)
        stats_box_layout.addWidget(self.stdDev_label)
        stats_box_layout.addWidget(self.kurt_label)
        stats_box_layout.addWidget(self.skew_label)
        stats_box_layout.addWidget(self.minVal_label)
        stats_box_layout.addWidget(self.maxVal_label)
        stats_box_layout.addWidget(self.range_label)
        stats_box_layout.addWidget(self.sumT_label)
        stats_box.setLayout(stats_box_layout)

        #Ignore the box creation for now, since the graph box would just have 1 widget
        #graph_box = QGroupBox("Data and Probability Graph")
        
        #Create some distribution options
        #Start with creating a check button.
        self.normal_checkbox = QCheckBox('Normal Distribution',self)
        # We want to run the plotting routine for the distribution, but 
        # we need to know the statistical values, so we'll calculate statistics
        # first.
        self.normal_checkbox.stateChanged.connect(self.compute_stats)
        
        #Repeat for additional distributions.
        self.log_checkbox = QCheckBox('Log-Normal Distribution',self)
        self.log_checkbox.stateChanged.connect(self.compute_stats)
        self.contin_checkbox = QCheckBox('Uniform Distribution',self)
        self.contin_checkbox.stateChanged.connect(self.compute_stats)
        self.triang_checkbox = QCheckBox('Triangular Distribution',self)
        self.triang_checkbox.stateChanged.connect(self.compute_stats)
        self.quad_checkbox = QCheckBox('U-Quadratic Distribution',self)
        self.quad_checkbox.stateChanged.connect(self.compute_stats)
        
        distribution_box = QGroupBox("Distribution Functions")
        distribution_box_layout= QVBoxLayout()
        distribution_box_layout.addWidget(self.normal_checkbox)
        distribution_box_layout.addWidget(self.log_checkbox)
        distribution_box_layout.addWidget(self.contin_checkbox)
        distribution_box_layout.addWidget(self.triang_checkbox)
        distribution_box_layout.addWidget(self.quad_checkbox)
        distribution_box.setLayout(distribution_box_layout)

        #Now we can set all the previously defined boxes into the main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(self.graph_canvas,0,1) 
        grid_layout.addWidget(distribution_box,1,1)
                
        main_widget.setLayout(grid_layout)

    def openingFile(self):
        fname, _filter = QFileDialog.getOpenFileName(self, 'Open file', 'C:')
        self.load_data(fname)
        
    def simpLoad(self):
        #for this example, we'll hard code the file name.
        #fileName = "Historical Temperatures from Moose Wyoming.csv"
        self.load_data('Historical Temperatures from Moose Wyoming.csv')#fileName)
           
    def load_data(self, fileName):   
       try:
           self.data_table.setRowCount(0)
       except:
           pass
       header_row = 1 
       #load data file into memory as a list of lines
       #print('{}'.format(fileName))    
       try:
           with open(fileName,'r') as data_file:
                self.data_lines = data_file.readlines()
            
           print("Opened {}".format(fileName))
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
       except:
           pass
    
    def compute_stats(self):
        #setup array
        item_list=[]
        items = self.data_table.selectedItems()
        #items=allItems[~np.isnan(allItems)] #mask for nan, pull true vals into new array
        for item in items:
            try:
                item_list.append(float(item.text()))
            except:
                pass
        
        if len(item_list) > 1: #Check to see if there are 2 or more samples
            data_array = np.asarray(item_list)
            data_array = np.asarray(item_list)
            mean_value = np.mean(data_array)
            medianVal=np.median(data_array)
            sumT=sum(item_list)
            length=len(item_list)
            minVal=np.amin(data_array)
            maxVal=np.amax(data_array)
            rangeVal=maxVal-minVal
            stdDev=np.std(data_array)
            kurt=stats.kurtosis(data_array)
            skew=stats.skew(data_array)
            try:
                #print("Mode {} rows.".format(collections.Counter(data_array).most_common(1)))
                modeVal=statistics.mode(data_array)
            except:
                modeVal=103
                pass
                
        if len(item_list)>2:
            varVal=statistics.variance(item_list)
        else:
            varVal=0
            
        try:
            #first number ,n, in {n:pf} is index of call in format()
            print("Mean = {0:8.6f} \tMedian= {1:8.6f} \tMode{3:4.1f}\tStandardDeviation= {2:8.6f}".format(mean_value, medianVal, stdDev, modeVal))
            print("  Kurtosis= {0:8.6f}\tSkew= {1:8.6f}\tVariance= {2:8.6f}".format(kurt, skew, varVal))
            print("  MinVal= {0:5.1f}\tMaxVal= {1:5.1f} \tRange= {2:5.1f}".format(minVal, maxVal, rangeVal))
            print("  Items Selected:{0:5.0f} with total sum of values:{1:5.0f} ".format(length, sumT))
            
            self.mean_label.setText("Mean = {:0.6f}".format(mean_value))
            self.median_label.setText("Median = {:0.6f}".format(medianVal))
            self.mode_label.setText("Mode = {:0.6f}".format(modeVal))
            self.stdDev_label.setText("StdDev = {:0.6f}".format(stdDev))
            self.kurt_label.setText("Kurtosis= {:0.6f}".format(kurt))
            self.skew_label.setText("Skew= {:0.6f}".format(skew))
            self.minVal_label.setText("Minimum= {:0.1f}".format(minVal))
            self.maxVal_label.setText("Maximum= {:0.1f}".format(maxVal))
            self.range_label.setText("Range = {:0.1f}".format(rangeVal))
            self.sumT_label.setText("Sum= {:0.1f}".format(sumT))
            if length<100:
                bins=math.floor(length/2)
            else:
                bins=50
            self.graph_canvas.plot_histogram(data_array, bins)
            if self.normal_checkbox.isChecked():
                self.graph_canvas.plot_normal(mean_value,stdDev)
            if self.contin_checkbox.isChecked():
                self.graph_canvas.plot_contin(maxVal, minVal)
            if self.quad_checkbox.isChecked():
                self.graph_canvas.plot_quad(maxVal, minVal)
            if self.log_checkbox.isChecked():
                self.graph_canvas.plot_log(mean_value, stdDev)    
            if self.triang_checkbox.isChecked():
                self.graph_canvas.plot_triang(maxVal, minVal, modeVal)        

                #add more distributions here
        except:
            pass

        
    
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
    execute = StatCalculator()
    sys.exit(app.exec_())
