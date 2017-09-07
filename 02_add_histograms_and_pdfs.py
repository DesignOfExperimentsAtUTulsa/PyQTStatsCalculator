# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 09:20:25 2017

@author: redwi
"""

#!/bin/env/python
# An introduction graphing some probability density functions
# 
# Assignment 2 in ME7863: Design and Analysis of Experiments
# Taught By Dr. Jeremy Daily
# Orignially assigned Fall 2017
#
# This is a gentle introduction to programming using Python, numpy, scipy, and PyQt5
# Examples from https://docs.scipy.org/doc/scipy/reference/tutorial/stats.html
# Import modules 
import sys,os
from PyQt5.QtWidgets import (QMainWindow,
                             QWidget,
                             QFileDialog, 
                             QLabel, 
                             QCheckBox, 
                             QVBoxLayout, 
                             QApplication, 
                             QPushButton,
                             QTableWidget, 
                             QTableWidgetItem,
                             QGroupBox,
                             QGridLayout,
                             QSizePolicy,
                             QMessageBox, QLineEdit)
from PyQt5.QtCore import QCoreApplication, Qt
import statistics
from scipy import stats
import numpy as np
#import the distributions to use
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import uniform
from scipy.stats import t
from scipy.stats import f
# add more here


from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

#Add a class for matplotlib graphs
# Code was inspired from the Internet
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
        FigureCanvas.mpl_connect(self,'button_press_event', self.double_click)
        
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
        
    def double_click(self, event):
        FigureCanvas.mpl_connect(self,'button_press_event', self.export)
        
class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself frequently with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.axes.set_xlabel("X Label")
        self.axes.set_ylabel("Y Label")
        self.axes.set_title("Title")
             
    def plot_histogram(self,data_array,data_label="Temperature",
                       title="Probability Density Function Plots",bins=50):
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
    
    def plot_random_variable(self,data,rv):
        print(rv)
        data_mean = np.mean(data)
        data_sigma = np.std(data)
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(xmin,xmax, 100) #x = np.linspace(loc-3*scale,loc+3*scale, 100)
        
        if (rv.name =='lognorm'):
          print(rv)
            #s is the shape parameter
          # See https://en.wikipedia.org/wiki/Log-normal_distribution
          # and https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html#scipy.stats.lognorm
          s = np.sqrt(np.log(1+data_sigma**2/data_mean**2))
          #shift to only use positive numbers
          y = rv.pdf(x,s,loc=0,scale=data_sigma)
          
        elif (rv.name == 'uniform'):
            
            y = rv.pdf(x)
            
        elif (rv.name == 't'):
          
            df = 1
            y = rv.pdf(x,df) 
            
        elif (rv.name == 'f'):
            df1 = 1
            df2 = 1
            y= F.pdf(x,df1, df2)

        else:
         print(rv)
         y = rv.pdf(x,loc=data_mean,scale=data_sigma)
         
        self.axes.plot(x,y,label=rv.name)
        self.axes.legend(shadow=True)
        self.draw()
        
class StatCalculator(QMainWindow):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              
    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,30,1000,700)

        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("Open .CSV File Type")
        file.triggered.connect(self.load_data)
        
        self.load_button = QPushButton('Load Data',self)
        self.load_button.clicked.connect(self.load_data)
     
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.stdError_label = QLabel("Standard Error: Not Computed Yet",self)
        self.median_label = QLabel("Median: Not Computed Yet",self)
        self.mode_label = QLabel("Mode: Not Computed Yet",self)
        self.stdDev_label = QLabel("Standard Deviation: Not Computed Yet",self)
        self.var_label = QLabel("Standard Variance: Not Computed Yet",self)
        self.kurt_label = QLabel("Kurtosis: Not Computed Yet",self)
        self.skew_label = QLabel("Skewness: Not Computed Yet",self)
        self.max_label = QLabel("Max: Not Computed Yet",self)
        self.min_label = QLabel("Min: Not Computed Yet",self)
        self.range_label = QLabel("Range: Not Computed Yet",self)
        self.sum_label = QLabel("Sum: Not Computed Yet",self)
        self.count_label = QLabel("Number of Entries: Not Computed Yet",self)
        
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        main_widget = QWidget()
        
        self.graph_canvas = MyDynamicMplCanvas(main_widget, width=5, height=4, dpi=100)
        
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
        stats_box_layout.addWidget(self.stdError_label)
        stats_box_layout.addWidget(self.mode_label)
        stats_box_layout.addWidget(self.stdDev_label)
        stats_box_layout.addWidget(self.var_label)
        stats_box_layout.addWidget(self.kurt_label)
        stats_box_layout.addWidget(self.skew_label)
        stats_box_layout.addWidget(self.max_label)
        stats_box_layout.addWidget(self.min_label)
        stats_box_layout.addWidget(self.range_label)
        stats_box_layout.addWidget(self.sum_label)
        stats_box_layout.addWidget(self.count_label)
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
        self.log_normal_checkbox = QCheckBox('Log-Normal Distribution',self)
        self.log_normal_checkbox.stateChanged.connect(self.compute_stats)
        
        self.uniform_checkbox = QCheckBox('Uniform',self)
        self.uniform_checkbox.stateChanged.connect(self.compute_stats)
       
        self.t_checkbox = QCheckBox('T Distribution', self)
        self.t_checkbox.stateChanged.connect(self.compute_stats)
       
        self.F_checkbox = QCheckBox('F Distribution', self)
        self.F_checkbox.stateChanged.connect(self.compute_stats)
        
        distribution_box = QGroupBox("Distribution Functions")
        distribution_box_layout= QVBoxLayout()
        distribution_box_layout.addWidget(self.normal_checkbox)
        distribution_box_layout.addWidget(self.log_normal_checkbox)
        distribution_box_layout.addWidget(self.uniform_checkbox)
        distribution_box_layout.addWidget(self.t_checkbox)
        distribution_box_layout.addWidget(self.F_checkbox)
        distribution_box.setLayout(distribution_box_layout)

        #Now we can set all the previously defined boxes into the main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(self.graph_canvas,0,1) 
        grid_layout.addWidget(distribution_box,1,1)
          
        main_widget.setLayout(grid_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle('Plotting Probability Density Functions - Dr. Daily\'s Example')
        self.show()
    
    def load_data(self):        
        #for this example, we'll hard code the file name.
        data_file_name = QFileDialog.getOpenFileName(self, 'Open File', '/')  
        #for the assignment, have a dialog box provide the filename

        #check to see if the file exists and then load it
        if os.path.exists(data_file_name[0]):
            header_row = 1 
            #load data file into memory as a list of lines       
            with open(data_file_name[0],'r') as data_file:
                self.data_lines = data_file.readlines()
        
            print("Opened {}".format(data_file_name))
            print(self.data_lines[1:10])
        
            #Set the headers
            #parse the lines by stripping the newline character off the end
            #and then splitting them on commas.
            data_table_columns = self.data_lines[header_row].strip().split(',')
            self.data_table.setColumnCount(len(data_table_columns))
            self.data_table.setHorizontalHeaderLabels(data_table_columns)

            #fill the table starting with the row after the header

            for row in range(header_row+1, len(self.data_lines)):
               #parse the data in memory into a list 
               row_values = self.data_lines[row].strip().split(',')
               #insert a new row
               current_row = self.data_table.rowCount()
               self.data_table.insertRow(current_row)
               
               #Populate the row with data
               for col in range(len(data_table_columns)):
                   entry = QTableWidgetItem("{}".format(row_values[col]))
                   self.data_table.setItem(current_row,col,entry)
            print("Filled {} rows.".format(row))
        
        else:
            print("File not found.")

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
            stdDev_value = np.std(data_array)
            stdError_value = stats.sem(data_array)
            median_value = np.median(data_array)
            mode_value = statistics.mode(data_array)
            var_value = np.var(data_array)
            kurt_value = stats.kurtosis(data_array)
            skew_value = stats.skew(data_array)
            max_value = max(data_array)
            min_value = min(data_array) 
            range_value = max_value-min_value
            sum_value = sum(data_array)
            count_value = len(data_array)
            
            #print("Mean = {0:5f}".format(mean_value))
            self.mean_label.setText("Mean = {0:3f} ".format(mean_value))
            #print("Standard Error = {0:5f} ".format(stdError_value))
            self.stdError_label.setText("Standard Error = {0:3f} ".format(stdError_value))
            #print("Median = {0:5f} ".format(median_value))
            self.median_label.setText("Median = {0:3f} ".format(median_value))
            #print("Mode = {0:5f} ".format(mode_value))
            self.mode_label.setText("Mode = {0:3f} ".format(mode_value))
            #print("Standard Deviation = {0:5f} ".format(stdDev_value))
            self.stdDev_label.setText("Standard Deviation = {0:3f} ".format(stdDev_value))
            #print("Stanard Variance = {0:5f} ".format(var_value))
            self.var_label.setText("Standard Variance = {0:3f} ".format(var_value))
            #print("Kurtosis = {0:5f} ".format(kurt_value))
            self.kurt_label.setText("Kurtosis = {0:3f} ".format(kurt_value))
            #print("Skew = {0:5f} ".format(skew_value))
            self.skew_label.setText("Skewness = {0:3f} ".format(skew_value))
            #print("Max = {0:5f} ".format(max_value))
            self.max_label.setText("Max = {0:3f} ".format(max_value))
            #print("Min = {0:5f} ".format(min_value))
            self.min_label.setText("Min = {0:3f} ".format(min_value))
            #print("Range  = {0:5f} ".format(range_value))
            self.range_label.setText("Range = {0:3f} ".format(range_value))
            #print("Sum = {0:5f} ".format(sum_value))
            self.sum_label.setText("Sum = {0:3f} ".format(sum_value))
            #print("Count = {0:5f} ".format(count_value))
            self.count_label.setText("Number of Entries = {0:3f} ".format(count_value))
            
            self.graph_canvas.plot_histogram(data_array)
            if self.normal_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,norm)
            if self.log_normal_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,lognorm)
            if self.uniform_checkbox.isChecked():
                self.graph_canvas.plot_uniform(data_array, uniform)
            if self.t_checkbox.isChecked():
                self.graph_canvas.plot_uniform(data_array, t)
            if self.F_checkbox.isChecked():
                self.graph_canvas.plot_uniform(data_array, t)
                #add more distributions here
        
'''       
  1. Add the ability to plot a normalized Histogram of the selected data in the table.*
  2. Add a menu option to open a CSV data file.*
  3. Add a checkbox for at least 5 distribution functions to plot over the top of the Histogram. 
    a. Include a legend and appropriate labels on your graph.
    b. Include axes labels. (Challenge: make the labels editable in your program).
  4. Use a grid style layout for your GUI*
  5. Save the plot to a PDF when you double click on it.*
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