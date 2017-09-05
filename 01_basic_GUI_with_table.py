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
from scipy import stats as st
import statistics as sts

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
        self.stats_button = QPushButton(b2)
        self.stats_button.setText('Compute Statistics')
        self.stats_button.clicked.connect(self.compute_stats)
        
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.error_label = QLabel("Error: Not Computed Yet",self)
        self.median_label = QLabel("Median: Not Computed Yet",self)
        self.mode_label = QLabel("Mode: Not Computed Yet",self)
        self.std_dev_label = QLabel("Standard deviation: Not Computed Yet",self)
        self.variance_label = QLabel("Variance: Not Computed Yet",self)
        self.kurtosis_label = QLabel("Kurtosis: Not Computed Yet",self)
        self.skewness_label = QLabel("Skewness: Not Computed Yet",self)
        self.range_label = QLabel("Range: Not Computed Yet",self)
        self.min_label = QLabel("Minimum: Not Computed Yet",self)
        self.max_label = QLabel("Maximum: Not Computed Yet",self)
        self.sum_label = QLabel("Sum: Not Computed Yet",self)
        self.count_label = QLabel("Count: Not Computed Yet",self)
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.stats_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.mean_label)
        v_layout.addWidget(self.error_label)
        v_layout.addWidget(self.median_label)
        v_layout.addWidget(self.mode_label)
        v_layout.addWidget(self.std_dev_label)
        v_layout.addWidget(self.variance_label)
        v_layout.addWidget(self.kurtosis_label)
        v_layout.addWidget(self.skewness_label)
        v_layout.addWidget(self.range_label)
        v_layout.addWidget(self.min_label)
        v_layout.addWidget(self.max_label)
        v_layout.addWidget(self.sum_label)
        v_layout.addWidget(self.count_label)
        
        self.setLayout(v_layout)
        self.setWindowTitle('Statistics Calculator GUI - Keagan Clement')
        self.activateWindow()
        self.raise_()
        self.show()
    
    def load_data(self):        
       #for this example, we'll hard code the file name.
       #root = tk.Tk()
       data_file_name = QFileDialog.getOpenFileName(QWidget())
       #data_file_name = input('Enter name of file: ')
       #data_file_name = "Historical Temperatures from Moose Wyoming.csv"
       print(data_file_name[0])
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
        error_value = st.stats.sem(data_array)
        median_value = np.median(data_array)
        mode_value = sts.mode(data_array)
        std_dev_value = np.std(data_array)
        variance_value = np.var(data_array)
        kurtosis_value = st.kurtosis(data_array)
        skewness_value = st.skew(data_array)
        min_value = min(item_list)
        max_value = max(item_list)
        sum_value = sum(item_list)
        
        print("Mean = {0:5f}".format(mean_value),"Median = {0:5f}".format(median_value),"Standard error = {0:5f}".format(error_value),"Mode = {0:5f}".format(mode_value),"Kurtosis = {0:5f}".format(kurtosis_value),"Skewness = {0:5f}".format(skewness_value),"Range = {0:5f}".format(max_value - min_value),"Minimum = {0:5f}".format(min_value),"Maximum = {0:5f}".format(max_value),"Sum = {0:5f}".format(sum_value),"Count = {0:5f}".format(sum_value / mean_value))
        self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
        self.error_label.setText("Standard error = {:0.3f}".format(error_value))
        self.median_label.setText("Median = {:0.3f}".format(median_value))
        self.mode_label.setText("Mode = {:0.3f}".format(mode_value))
        self.std_dev_label.setText("Standard deviation = {:0.3f}".format(std_dev_value))
        self.variance_label.setText("Variance = {:0.3f}".format(variance_value))
        self.kurtosis_label.setText("Kurtosis = {:0.3f}".format(kurtosis_value))
        self.skewness_label.setText("Skewness = {:0.3f}".format(skewness_value))
        self.range_label.setText("Range = {:0.3f}".format(max_value - min_value))
        self.min_label.setText("Minimum = {:0.3f}".format(min_value))
        self.max_label.setText("Maximum = {:0.3f}".format(max_value))
        self.sum_label.setText("Sum = {:0.3f}".format(sum_value))
        self.count_label.setText("Count = {:0.3f}".format(sum_value / mean_value))
        
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
