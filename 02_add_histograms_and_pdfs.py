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
                             QAction,
                             QMessageBox,
                             QSizePolicy)

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt

import numpy as np
from scipy import stats
#import the distributions to use
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import laplace
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
        data_sigma = np.std(data) #Sigma = Std dev
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(xmin,xmax, 100) #x = np.linspace(loc-3*scale,loc+3*scale, 100)
        
        if rv.name =='lognorm':
          #s is the shape parameter
          # See https://en.wikipedia.org/wiki/Log-normal_distribution
          # and https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html#scipy.stats.lognorm
          s = np.sqrt(np.log(1+data_sigma**2/data_mean**2))
          #shift to only use positive numbers
          y = rv.pdf(x,s,loc=0,scale=data_sigma)
          print("Finished Drawing Lognormal Distribution.")
          
        else:
          y = rv.pdf(x,loc=data_mean,scale=data_sigma)
          
        self.axes.plot(x,y,label=rv.name)
        self.axes.legend(shadow=True)
        self.draw()
  #-----------------------------------------------------------------------              
    def plot_T(self,data,sigma):
        xmin,xmax = self.axes.get_xlim()
        df = 2
        data_mean = np.mean(data)
        loc= data_mean
        scale= 15        

        x = np.linspace(xmin,xmax, 100)
        y = t.pdf(x, df, loc, scale)

        self.axes.plot(x,y,label="T distribution")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing T Distribution.")  
        
    def plot_F(self,data,sigma):
        xmin,xmax = self.axes.get_xlim()
        dfn= 10
        dfd= 10 
        data_mean = np.mean(data)
        loc= data_mean
        scale= 15        
        
        x = np.linspace(xmin,xmax, 100)
        y = f.pdf(x, dfn, dfd, loc, scale)
      
        self.axes.plot(x,y,label="F distribution")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing F Distribution.")
        
    def plot_laplace(self,mu,sigma):
        xmin,xmax = self.axes.get_xlim()
        data_mean = np.mean(mu)
        x = np.linspace(mu-3*sigma,mu+3*sigma, 100)
        
        loc= data_mean
        scale= 15
        y = laplace.pdf(x, loc, scale)
        
        self.axes.plot(x,y,label="Laplace")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Laplace Distribution.")  
  
#-----------------------------------------------------------------------        
class StatCalculator(QMainWindow):
  
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"file to open", "", "CSV (*.csv)", options=options)
        if fileName:
            print(fileName)
            self.load_data(fileName)          
          
    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              
    def init_ui(self):
        #Builds GUI
        self.setGeometry(100,100,1700,800)
        
        menubar = self.menuBar()
        file = menubar.addMenu('File')
        action = QAction('Load file',self)
        file.addAction(action)
        action.triggered.connect(self.openFileNameDialog)
     
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.std_label = QLabel("Std Dev: Not Computed Yet",self)
        self.sterror_label = QLabel("Standard_error: Not Computed Yet",self)    #Nuevo
        self.median_label = QLabel("Median: Not Computed Yet",self)             #Nuevo
        self.mode_label = QLabel("Mode: Not Computed Yet",self)                 #Nuevo
        self.variance_label = QLabel("Variance: Not Computed Yet",self)         #Nuevo
        self.kurtosis_label = QLabel("Kurtosis: Not Computed Yet",self)         #Nuevo
        self.skewness_label = QLabel("Skewness: Not Computed Yet",self)         #Nuevo
        self.range_label = QLabel("Range: Not Computed Yet",self)               #Nuevo
        self.min_label = QLabel("Minimum: Not Computed Yet",self)               #Nuevo
        self.max_label = QLabel("Maximum: Not Computed Yet",self)               #Nuevo
        self.sum_label = QLabel("Sum: Not Computed Yet",self)                   #Nuevo
        self.count_label = QLabel("Count: Not Computed Yet",self)               #Nuevo     
        
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

        table_box_layout.addWidget(self.data_table)
        #setup the layout to be displayed in the box
        table_box.setLayout(table_box_layout)
        
        #repeat the box layout for Statistics
        stats_box = QGroupBox("Summary Statistics")
        stats_box_layout = QVBoxLayout()
        stats_box_layout.addWidget(self.mean_label)
        stats_box_layout.addWidget(self.std_label)
        stats_box_layout.addWidget(self.sterror_label)      #nuevo
        stats_box_layout.addWidget(self.median_label)       #nuevo
        stats_box_layout.addWidget(self.mode_label)         #nuevo
        stats_box_layout.addWidget(self.variance_label)     #nuevo
        stats_box_layout.addWidget(self.kurtosis_label)     #nuevo
        stats_box_layout.addWidget(self.skewness_label)     #nuevo
        stats_box_layout.addWidget(self.range_label)        #nuevo
        stats_box_layout.addWidget(self.min_label)          #nuevo
        stats_box_layout.addWidget(self.max_label)          #nuevo
        stats_box_layout.addWidget(self.sum_label)          #nuevo
        stats_box_layout.addWidget(self.count_label)        #nuevo
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
        
        self.T_checkbox = QCheckBox('T Distribution',self)              #nuevo
        self.T_checkbox.stateChanged.connect(self.compute_stats)  
        
        self.F_checkbox = QCheckBox('F Distribution',self)              #nuevo
        self.F_checkbox.stateChanged.connect(self.compute_stats)  
        
        self.laplace_checkbox = QCheckBox('Laplace Distribution',self)              #nuevo
        self.laplace_checkbox.stateChanged.connect(self.compute_stats)
 
       
        distribution_box = QGroupBox("Distribution Functions")
        distribution_box_layout= QVBoxLayout()
        distribution_box_layout.addWidget(self.normal_checkbox)
        distribution_box_layout.addWidget(self.log_normal_checkbox)
        distribution_box_layout.addWidget(self.T_checkbox)
        distribution_box_layout.addWidget(self.F_checkbox)                #nuevo
        distribution_box_layout.addWidget(self.laplace_checkbox)                #nuevo
        
        distribution_box.setLayout(distribution_box_layout)

        #Now we can set all the previously defined boxes into the main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(self.graph_canvas,0,1) 
        grid_layout.addWidget(distribution_box,1,1)
          
        main_widget.setLayout(grid_layout)
        self.setCentralWidget(main_widget)
        self.setWindowTitle('Homework #2 by Cristian Nunez ')
        self.show()
    
    def load_data(self,fileN):        
#for this example, we'll hard code the file name.
        data_file_name = fileN
        #for the assignment, have a dialog box provide the filename
        #check to see if the file exists and then load it
        if os.path.exists(data_file_name):
            header_row = 1 
        #load data file into memory as a list of lines       
        with open(data_file_name,'r') as data_file:
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
        
    #else:
     #   print("File not found.")

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
            suma = np.sum (item_list) #Nuevo
            error = stats.tsem(item_list) #Nuevo
            median = np.median (item_list)  #Nuevo
            variance = stats.tvar(item_list)  #Nuevo
            kurtosis = stats.kurtosis (item_list)  #Nuevo
            skewness = stats.skew (item_list)  #Nuevo
            minimum = stats.tmin(item_list)  #Nuevo
            maximum = stats.tmax(item_list)  #Nuevo
            count = len (item_list)       #Nuevo
            rango = int(maximum) - int(minimum) #Nuevo
            mode = np.array(stats.mode(item_list))  #Nuevo
            mode_value = mode[0]
            
            print("Mean = {0:5f}".format(mean_value))
            self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
            self.std_label.setText("Std Dev = {:0.4f}".format(stdev_value))
            self.sum_label.setText("Sum = {:0.3f}".format(suma))
            self.sterror_label.setText("Standard error = {:0.3f}".format(error))
            self.median_label.setText("Median = {:0.3f}".format(median))
            self.variance_label.setText("Variance = {:0.3f}".format(variance))
            self.kurtosis_label.setText("Kurtosis = {:0.3f}".format(kurtosis))
            self.skewness_label.setText("Skewness = {:0.3f}".format(skewness))
            self.min_label.setText("Minimum = {:0.3f}".format(minimum))
            self.max_label.setText("Maximum = {:0.3f}".format(maximum))
            self.count_label.setText("Count = {:0.3f}".format(count))
            self.range_label.setText("Range = {:0.3f}".format(rango))
            self.mode_label.setText("Mode = {:0.3f}".format(mode_value[0]))
            
            self.graph_canvas.plot_histogram(data_array)
            if self.normal_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,norm)
                
            if self.log_normal_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,lognorm)
                
            if self.T_checkbox.isChecked():           
                self.graph_canvas.plot_T(mean_value, stdev_value)
                
            if self.F_checkbox.isChecked():           
                self.graph_canvas.plot_F(mean_value, stdev_value)
                
            if self.laplace_checkbox.isChecked():           
                self.graph_canvas.plot_laplace(mean_value, stdev_value)            
        
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
