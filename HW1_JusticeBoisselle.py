#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem, QInputDialog, QLineEdit)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication

import numpy as np

import scipy.stats

import statistics

from PyQt5.QtGui import QIcon

class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              

    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,500,500)
        
        

        b1 = QWidget()
        self.get_button = QPushButton(b1)
        self.get_button.setText('set file address')
        self.get_button.clicked.connect(self.get_address)
        
        b2 = QWidget()
        self.load_button = QPushButton(b2)
        self.load_button.setText('Load Data')
        self.load_button.clicked.connect(self.load_data)
        
        b3 = QWidget()
        self.stats_button = QPushButton(b3)
        self.stats_button.setText('Compute Statistics')
        self.stats_button.clicked.connect(self.compute_stats)
        
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.get_button)
        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.stats_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.mean_label)
        
        self.setLayout(v_layout)
        self.setWindowTitle('Introduction to Descriptive Statistics-Justice Boisselle')
        self.activateWindow()
        self.raise_()
        self.show()
    
    def get_address(self):
        address, okPressed = QInputDialog.getText(self, "data","address of data file", QLineEdit.Normal, "")
        if okPressed and address != '':
            print(address)
        global file_address 
        file_address = address
    
    
    def load_data(self):   

       
       data_file_name = file_address
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
        standard_error = np.std(data_array)
        median= np.median(data_array)
        mode = statistics.mode(item_list)
        standard_div = np.std(data_array)
        variance = np.var(data_array)
        kurtosis = scipy.stats.kurtosis(data_array)
        skew = scipy.stats.skew(data_array)
        data_range = np.ptp(data_array)
        minimum = np.amin(data_array)
        maximum = np.amax(data_array)
        summation = np.sum(data_array)
        count = len(data_array)
        large = maximum
        small = minimum
        confidence = scipy.stats.t.interval(0.95, count, loc = 1, scale = 1)
#        
        print("Mean = {0:5f}".format(mean_value))
        print("Standard Error = {0:5f}".format(standard_error))
        print("Median = {0:5f}".format(median))
        print("Mode = {0:5f}".format(mode))
        print("Standard Deviation = {0:5f}".format(standard_div))
        print("Variance = {0:5f}".format(variance))
        print("Kurtosis = {0:5f}".format(kurtosis))
        print("Skewness = {0:5f}".format(skew))
        print("Range = {0:5f}".format(data_range))
        print("Minimum = {0:5f}".format(minimum))
        print("Maximum = {0:5f}".format(maximum))
        print("Sum = {0:5f}".format(summation))
        print("Count = {0:5f}".format(count))
        print("Largest = {0:5f}".format(large))
        print("Smallest = {0:5f}".format(small))
        print("Confidence = {0:5f}".format(confidence))


        self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
        
    
            
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
