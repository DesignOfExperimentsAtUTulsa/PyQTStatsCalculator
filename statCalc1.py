# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication

import numpy as np #np is a pointer to the numpy library, hence np.fn() calls a numpy subfunction

class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              

    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,500,500)

        b1 = QWidget()
        self.load_button = QPushButton(b1)
        self.load_button.setText('Load Data')
        self.load_button.clicked.connect(self.load_data)
        
        b2 = QWidget()
        self.stats_button = QPushButton(b1)
        self.stats_button.setText('Compute Statistics')
        self.stats_button.clicked.connect(self.compute_stats)
        
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.median_label = QLabel("Median: Not Computed Yet",self)
        self.stdDev_label = QLabel("Standard Deviation: Not Computed Yet",self)
        self.range_label = QLabel("Range: Not Computed Yet",self)
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.stats_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.mean_label)
        v_layout.addWidget(self.median_label)
        v_layout.addWidget(self.stdDev_label)
        v_layout.addWidget(self.range_label)
        
        self.setLayout(v_layout)
        self.setWindowTitle('AustinVs Calc: Introduction to Descriptive Statistics')
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
        mean_value = np.mean(data_array)
        medianVal=np.median(data_array)
        stdDev=np.std(data_array)
        minVal=np.amin(data_array)
        maxVal=np.amax(data_array)
        rangeVal=maxVal-minVal
        #first number ,n, in {n:pf} is index of call in format()
        print("Mean = {0:5f} \tMedian={1:5f} \tStandardDeviation={2:5f}".format(mean_value, medianVal, stdDev))
        print("\tMinVal={0:5f} \tMaxVal={1:5f} \tRange={2:5f}".format(minVal, maxVal, rangeVal))
        self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
        self.median_label.setText("Median = {:0.3f}".format(medianVal))
        self.stdDev_label.setText("StdDev = {:0.3f}".format(stdDev))
        self.range_label.setText("Range = {:0.3f}".format(rangeVal))
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
