#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication

import numpy as np
import math
from scipy import stats
import statistics

class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              

    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,500,800)

        b1 = QWidget()
        self.load_button = QPushButton(b1)
        self.load_button.setText('Load Data')
        self.load_button.clicked.connect(self.load_data)
        
        b2 = QWidget()
        self.stats_button = QPushButton(b1)
        self.stats_button.setText('Compute Statistics')
        self.stats_button.clicked.connect(self.compute_stats)
        
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.stderr_label = QLabel("Std Error: Not Computed Yet", self)
        self.med_label = QLabel("Median: Not Computed Yet", self)
        self.mode_label = QLabel("Mode: Not Computed Yet", self)
        self.stddev_label = QLabel("Std Dev: Not Computed Yet", self)
        self.splvar_label = QLabel("Spl Variance: Not Computed Yet", self)
        self.kurt_label = QLabel("Kurtosis: Not Computed Yet", self)
        self.skw_label = QLabel("Skewness: Not Computed Yet", self)
        self.range_label = QLabel("Range: Not Computed Yet", self)
        self.min_label = QLabel("Min: Not Computed Yet", self)
        self.max_label = QLabel("Max: Not Computed Yet", self)
        self.sum_label = QLabel("Sum: Not Computed Yet", self)
        self.count_label = QLabel("Count: Not Computed Yet", self)
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.stats_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.mean_label)
        v_layout.addWidget(self.stderr_label)
        v_layout.addWidget(self.med_label)
        v_layout.addWidget(self.mode_label)
        v_layout.addWidget(self.stddev_label)
        v_layout.addWidget(self.splvar_label)
        v_layout.addWidget(self.kurt_label)
        v_layout.addWidget(self.skw_label)
        v_layout.addWidget(self.range_label)
        v_layout.addWidget(self.min_label)
        v_layout.addWidget(self.max_label)
        v_layout.addWidget(self.sum_label)
        v_layout.addWidget(self.count_label)
        
        self.setLayout(v_layout)
        self.setWindowTitle('Anvar Akhiiartdinov_HW1')
        self.activateWindow()
        self.raise_()
        self.show()
    
    def load_data(self):        
       
        #get the file path
       filename = QFileDialog.getOpenFileName(self, 'Open file',
                                              'MyFiles/Tulsa/Semester 3/Eng Exper/HW/HW1&2/PyQTStatsCalculator-master', '*.csv')
       
       print('filename', filename, '\n')
       with open(filename[0],'r') as data_file:
            self.data_lines = data_file.readlines()
           
       print("Opened {}".format(filename[0]))
       print(self.data_lines[1:10])
        
       #Set the headers
       #parse the lines by stripping the newline character off the end
       #and then splitting them on commas.
       header_row = 1 
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
        data_array = np.asarray(item_list)
        mean_value = np.mean(data_array)
        stderr_value = stats.sem(data_array, axis=None, ddof=0)
        med_value = np.median(data_array)
        mode_value = statistics.mode(data_array)
        stddev_value = np.std(data_array)
        splvar_value = np.var(data_array)
        kurt_value = stats.kurtosis(data_array)
        skw_value = stats.skew(data_array)
        range_value = np.ptp(data_array)
        min_value = np.min(data_array)
        max_value = np.max(data_array)
        sum_value = np.sum(data_array)
        count_value = len(data_array)
                             
        print("Mean = {0:5f}".format(mean_value))
                
        self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
        self.stderr_label.setText("Std Error = {:0.3f}".format(stderr_value))
        self.med_label.setText("Median = {:0.1f}".format(med_value))
        self.mode_label.setText("Mode = {:0.1f}".format(mode_value))
        self.stddev_label.setText("Std Dev = {:0.3f}".format(stddev_value))
        self.splvar_label.setText("Spl Variance = {:0.3f}".format(splvar_value))
        self.kurt_label.setText("Kurtosis = {:0.3f}".format(kurt_value))
        self.skw_label.setText("Skewness = {:0.3f}".format(skw_value))
        self.range_label.setText("Range = {:0.1f}".format(range_value))
        self.min_label.setText("Min = {:0.1f}".format(min_value))
        self.max_label.setText("Max = {:0.1f}".format(max_value))
        self.sum_label.setText("Sum = {:0.1f}".format(sum_value))
        self.count_label.setText("Count = {:0.1f}".format(count_value))
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
