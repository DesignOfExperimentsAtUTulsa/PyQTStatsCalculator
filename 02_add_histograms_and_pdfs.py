# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 11:46:27 2017

@author: Daniel
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
                             QAction,
                             QMenu,
                             QWidget as QW,
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
                             QMessageBox)
from PyQt5.QtCore import QCoreApplication

import numpy as np
#import the distributions to use
from scipy.stats import (norm, lognorm,
                         kurtosis,skew,
                         sem,t,f,cauchy,
                         vonmises_line)
import statistics
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
        #msg.setWindowModality(QW.Qt.ApplicationModal)
        msg.exec_()
        print("Exported PDF file")
        
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
        data_mean = np.mean(data)
        data_sigma = np.std(data)
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(xmin,xmax, 100) #x = np.linspace(loc-3*scale,loc+3*scale, 100)
               
        if rv.name =='lognorm':
            #print ("rv name =",rv.name)
            #print("rv =",rv)
            #s is the shape parameter
            # See https://en.wikipedia.org/wiki/Log-normal_distribution
            # and https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html#scipy.stats.lognorm
                        
            s = np.sqrt(np.log(1+data_sigma**2/data_mean**2))
            params = lognorm.fit(data,floc =0)
            #print (params)
            
            #shift to only use positive numbers
            y = rv.pdf(x,s,loc=params[1],scale=params[2])
            name = 'LogNormal'
        
        elif rv.name == 't':
            y= rv.pdf(x-data_mean,(len(data))-1,scale = data_sigma)
            name = 'T-distribution'
        
        elif rv.name == 'cauchy':
            params = cauchy.fit(data)
            y = rv.pdf(x,loc = params[0],scale =params[1])
            name = 'Isnt this title Cauchy?'
       
        elif rv.name =='vonmises_line':
            print('its vonmises time')
            #ranger = xmax-xmin
            #x1 = np.linspace(-np.pi,np.pi,100)
            
            #print('hey man, the data =',data_new)
            params = rv.fit(data)
            print(params)
            y= rv.pdf(x,params[0],loc = params[1], scale = params[2])
            name =('VonMises')
            
        else: #Normal
            y = rv.pdf(x,loc=data_mean,scale=data_sigma)
            name = 'Normal Bro'
        self.axes.plot(x,y,label = name)
        self.axes.legend(shadow=True)
        self.draw()
        
    
class StatCalculator(QMainWindow):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              
    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,1000,700)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        file_open = QAction('Open CSV File type',self)
        fileMenu.addAction(file_open)
        fileMenu.triggered[QAction].connect(self.load_data)
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setRowCount(13)
        stats1 = ["Mean","Standard Error","Median","Mode","Standard Deviation","Sample Variance","Kurtosis","Skewness","Range","Minimum","Maximum","Sum","Count"]
        for index in range(len(stats1)):
            self.stats_table.setItem(index,0,QTableWidgetItem(stats1[index]))
            self.stats_table.setItem(index,1,QTableWidgetItem('Not yet computed'))
        
        self.load_button = QPushButton('Load Data',self)
        self.load_button.clicked.connect(self.load_data)
     
                
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        main_widget = QW()
        
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
        stats_box_layout.addWidget(self.stats_table)
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
        
        self.t_distribution_checkbox = QCheckBox('T Distribution',self)
        self.t_distribution_checkbox.stateChanged.connect(self.compute_stats)
        
        #self.f_distribution_checkbox = QCheckBox('F Distribution',self)
        #self.f_distribution_checkbox.stateChanged.connect(self.compute_stats)
        
        self.cauchy_checkbox = QCheckBox('Cauchy Distribution',self)
        self.cauchy_checkbox.stateChanged.connect(self.compute_stats)
        
        self.von_misses_checkbox = QCheckBox('Von-Misses Distribution',self)
        self.von_misses_checkbox.stateChanged.connect(self.compute_stats)
        
        distribution_box = QGroupBox("Distribution Functions")
        distribution_box_layout= QVBoxLayout()
        distribution_box_layout.addWidget(self.normal_checkbox)
        distribution_box_layout.addWidget(self.log_normal_checkbox)
        distribution_box_layout.addWidget(self.t_distribution_checkbox)
        #distribution_box_layout.addWidget(self.f_distribution_checkbox)
        distribution_box_layout.addWidget(self.cauchy_checkbox)
        distribution_box_layout.addWidget(self.von_misses_checkbox)
        distribution_box.setLayout(distribution_box_layout)

        #Now we can set all the previously defined boxes into the main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(self.graph_canvas,0,1) 
        grid_layout.addWidget(distribution_box,1,1)
          
        main_widget.setLayout(grid_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle('Plotting Probability Density Functions - Daniel Moses')
        self.show()
    
    def load_data(self):        
        #for this example, we'll hard code the file name.
        data_file_name = QFileDialog.getOpenFileName(self,'open file')
        #data_file_name = "Historical Temperatures from Moose Wyoming.csv"
        #for the assignment, have a dialog box provide the filename

        #check to see if the file exists and then load it
        if os.path.exists(data_file_name[0]):
            header_row = 1 
            #load data file into memory as a list of lines       
            with open(data_file_name[0],'r') as data_file:
                self.data_lines = data_file.readlines()
        
            print("Opened {}".format(data_file_name[0]))
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
            
            #q75, q25 = np.percentile(data_array, [75 ,25])
            #iqr = q75 - q25
            
            mean_value = np.mean(data_array)
            stdev_value = np.std(data_array)
            median_value = np.median(data_array)
            variance = np.var(data_array)
            kurt = kurtosis(data_array, axis =0, fisher =True, bias = True)
            skew_ = skew(data_array, bias = True)
            standard_err = sem(data_array, axis =0)
            min_val = min(data_array)
            max_val = max(data_array)
            range_val = max_val-min_val
            mode = statistics.mode(data_array)
            count = len(data_array)
            summ = sum(data_array)
        
        #stat_format =QTableWidgetItem("{:.3f}".format(stat_value))
            stats_values = [mean_value,standard_err,median_value,mode,stdev_value,variance,kurt,skew_,
                        range_val,min_val,max_val,summ,count]
        
            for index in range(len(stats_values)):
                self.stats_table.setItem(index,1,QTableWidgetItem("{:.3f}".format(stats_values[index])))
            
            
            self.graph_canvas.plot_histogram(data_array)
            if self.normal_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,norm)
            if self.log_normal_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,lognorm)
            if self.t_distribution_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,t) 
            #if self.f_distribution_checkbox.isChecked():
               # self.graph_canvas.plot_f_distribution(data_array)
            if self.cauchy_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,cauchy)
            if self.von_misses_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,vonmises_line)
            
            #add more distributions here
        
'''       
  check1. Add the ability to plot a normalized Histogram of the selected data in the table.
  check2. Add a menu option to open a CSV data file.
  check3. Add a checkbox for at least 5 distribution functions to plot over the top of the Histogram. 
      checka. Include a legend and appropriate labels on your graph.
    b. Include axes labels. (Challenge: make the labels editable in your program).
  check4. Use a grid style layout for your GUI
  check5. Save the plot to a PDF when you double click on it.
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