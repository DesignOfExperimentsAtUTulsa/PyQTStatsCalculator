#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from scipy import stats
import numpy as np

class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              

    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,800,800)

        b1 = QWidget()
        self.load_button = QPushButton(b1)
        self.load_button.setText('Load Data')
        self.load_button.clicked.connect(self.openFileNameDialog)
        
        b2 = QWidget()
        self.stats_button = QPushButton(b2)
        self.stats_button.setText('Compute Statistics')
        self.stats_button.clicked.connect(self.compute_stats)
        
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.sterror_label = QLabel("Standard_error: Not Computed Yet",self)#Nuevo
        self.median_label = QLabel("Median: Not Computed Yet",self)#Nuevo
        self.mode_label = QLabel("Mode: Not Computed Yet",self)#Nuevo
        self.stdev_label = QLabel("Standard_deviation: Not Computed Yet",self)#Nuevo
        self.variance_label = QLabel("Variance: Not Computed Yet",self)#Nuevo
        self.kurtosis_label = QLabel("Kurtosis: Not Computed Yet",self)#Nuevo
        self.skewness_label = QLabel("Skewness: Not Computed Yet",self)#Nuevo
        self.range_label = QLabel("Range: Not Computed Yet",self)#Nuevo
        self.min_label = QLabel("Minimum: Not Computed Yet",self)#Nuevo
        self.max_label = QLabel("Maximum: Not Computed Yet",self)#Nuevo
        self.sum_label = QLabel("Sum: Not Computed Yet",self)#Nuevo
        self.count_label = QLabel("Count: Not Computed Yet",self) #Nuevo
        
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.stats_button)
        v_layout.addWidget(self.data_table)
       
        v_layout.addWidget(self.mean_label)
        v_layout.addWidget(self.sterror_label)
        v_layout.addWidget(self.median_label)
        v_layout.addWidget(self.mode_label)
        v_layout.addWidget(self.stdev_label)
        v_layout.addWidget(self.variance_label)
        v_layout.addWidget(self.kurtosis_label)
        v_layout.addWidget(self.skewness_label)
        v_layout.addWidget(self.range_label)
        v_layout.addWidget(self.min_label)
        v_layout.addWidget(self.max_label)
        v_layout.addWidget(self.sum_label)
        v_layout.addWidget(self.count_label)
        
        self.setLayout(v_layout)
        self.setWindowTitle('Introduction to Descriptive Statistics, By Cristian Nunez')
        self.activateWindow()
        self.raise_()
        self.show()
        
    
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"file to open", "", "CSV (*.csv)", options=options)
        if fileName:
            print(fileName)
            self.load_data(fileName)
 
   
    
    def load_data(self,fileN):        
       #for this example, we'll hard code the file name.
      # data_file_name = "Historical Temperatures from Moose Wyoming.csv"
       data_file_name = fileN
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
        data_array = np.asarray(item_list)
        
    
    #-----------------------------------------------------------------------------------------------------    
        
        mean_value = np.mean(data_array)        
        print("Mean = {0:5f}".format(mean_value))
        self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
        
        suma = np.sum (item_list)
        print("Sum = {0:5f}".format(suma))
        self.sum_label.setText("Sum = {:0.3f}".format(suma))
        
        error = stats.tsem(item_list)
        print("Standard Error = {0:5f}".format(error))
        self.sterror_label.setText("Standard error = {:0.3f}".format(error))
        
        median = np.median (item_list)
        print("Median = {0:5f}".format(median))
        self.median_label.setText("Median = {:0.3f}".format(median))
        
        standard_dev = stats.tstd(item_list)
        print("Standard deviation = {0:5f}".format(standard_dev))
        self.stdev_label.setText("Standard deviation = {:0.3f}".format(standard_dev))
                
        variance = stats.tvar(item_list)
        print("Variance = {0:5f}".format(variance)) 
        self.variance_label.setText("Variance = {:0.3f}".format(variance))
        
        kurtosis = stats.kurtosis (item_list)
        print("Kurtosis = {0:5f}".format(kurtosis))
        self.kurtosis_label.setText("Kurtosis = {:0.3f}".format(kurtosis))
        
        skewness = stats.skew (item_list)
        print("Skewness = {0:5f}".format(skewness)) 
        self.skewness_label.setText("Skewness = {:0.3f}".format(skewness))
        
        minimum = stats.tmin(item_list)
        print("Minimum = {0:5f}".format(minimum))
        self.min_label.setText("Minimum = {:0.3f}".format(minimum))
        
        maximum = stats.tmax(item_list)
        print("Maximum = {0:5f}".format(maximum))
        self.max_label.setText("Maximum = {:0.3f}".format(maximum))
        
        count = len (item_list)       
        print ('Count = ' , count)   #Nuevo
        self.count_label.setText("Count = {:0.3f}".format(count))
        
        rango = int(maximum) - int(minimum)
        print("Range = {0:5f}".format(rango))
        self.range_label.setText("Range = {:0.3f}".format(rango))
        
        mode = np.array(stats.mode(item_list))
        mode_value = mode[0]
        print("Mode = {0:5f}".format(mode_value[0]))
        self.mode_label.setText("Mode = {:0.3f}".format(mode_value[0])) #Este no quiere andar
        
  #Nuevo
        
        #-------------------------------------------------------------------
'''       
Assignment: 
1. Add all the quantities from the MS Excel descriptive Statistics 
add-in to automatically calculate and display. Demonstrate the results
from this program match Excel. Use the same dataset.
2. Add a dialog box to open and load any Comma Separated Values table. 
'''

if __name__ == '__main__':
    #Start the program this way according to https://stackoverflow.com/questions/40094086/python-kernel-dies-for-second-run-of-pyqt5-gui
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    execute = StatCalculator()
    sys.exit(app.exec_())
