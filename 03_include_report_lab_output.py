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

import numpy as np

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
          
    def plot_normal(self,mu,sigma):
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(mu-3*sigma,mu+3*sigma, 100)
        y = mlab.normpdf(x, mu, sigma)
        self.axes.plot(x,y,label="Normal")
        self.axes.legend(shadow=True)
        self.draw()
        print("Finished Drawing Normal Distribution.")
        
class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              
    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,1000,500)

        self.load_button = QPushButton('Load Data',self)
        self.load_button.clicked.connect(self.load_data)
     
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.std_label = QLabel("Std Dev: Not Computed Yet",self)
        
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
        stats_box_layout.addWidget(self.std_label)
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
        
        distribution_box = QGroupBox("Distribution Functions")
        distribution_box_layout= QVBoxLayout()
        distribution_box_layout.addWidget(self.normal_checkbox)
        distribution_box_layout.addWidget(self.log_normal_checkbox)
        distribution_box.setLayout(distribution_box_layout)

        #Now we can set all the previously defined boxes into the main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(self.graph_canvas,0,1) 
        grid_layout.addWidget(distribution_box,1,1)
        
        self.setLayout(grid_layout)
        
        self.setWindowTitle('Introduction to Descriptive Statistics - Dr. Daily\'s Example')
        self.activateWindow()
        self.raise_()
        self.show()
    
    def load_data(self):        
       #for this example, we'll hard code the file name.
       data_file_name = "Historical Temperatures from Moose Wyoming.csv"
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
            
            print("Mean = {0:5f}".format(mean_value))
            self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
            self.std_label.setText("Std Dev = {:0.4f}".format(stdev_value))
            
            self.graph_canvas.plot_histogram(data_array)
            if self.normal_checkbox.isChecked():
                self.graph_canvas.plot_normal(mean_value,stdev_value)
                #add more distributions here
        
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
