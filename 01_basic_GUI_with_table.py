# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 14:29:53 2017

@author: cwv414
"""

#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem, QMainWindow)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication

import numpy as np
from scipy import stats



class StatsMainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        
        
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Chris Vasquez HW1 Stats Calculator')    
        self.show()
        t=StatCalculator()
        self.setCentralWidget(t)
        
        
class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              

    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,500,500)

        self.load_button=QPushButton('Load Data', self)
        self.load_button.clicked.connect(self.load_data)
        
        
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
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.mean_label)
        v_layout.addWidget(self.stderr_label)
        v_layout.addWidget(self.median_label)
        v_layout.addWidget(self.mode_label)
        v_layout.addWidget(self.std_label)
        v_layout.addWidget(self.var_label)
        v_layout.addWidget(self.kurt_label)
        v_layout.addWidget(self.skew_label)
        v_layout.addWidget(self.range_label)
        v_layout.addWidget(self.min_label)
        v_layout.addWidget(self.max_label)
        v_layout.addWidget(self.sum_label)
        v_layout.addWidget(self.count_label)
        

        
        self.setLayout(v_layout)
        self.setWindowTitle('Introduction to Descriptive Statistics')
        self.activateWindow()
        self.raise_()
        self.show()
    
    def load_data(self):        
       #for this example, we'll hard code the file name.
       options=QFileDialog.Options()
       options|=QFileDialog.DontUseNativeDialog
       data_file_name, _ = QFileDialog.getOpenFileName(self,"Open CSV File", "", "All Files (*);;CSV Files (*.csv)", options=options)
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

        if len(item_list)>1:
            print(len(item_list))
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
    execute = StatsMainWindow()
    sys.exit(app.exec_())
