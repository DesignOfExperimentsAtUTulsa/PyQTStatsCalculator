#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem, QMainWindow, QTextEdit, 
                             QAction,)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication

import numpy as np

from scipy import stats

import statistics

class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              

    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,50,600,1000)

        self.load_button = QPushButton('Load Data',self)
        self.load_button.clicked.connect(self.load_data)
                        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setRowCount(13)
        stats1 = ["Mean","Standard Error","Median","Mode","Standard Deviation","Sample Variance","Kurtosis","Skewness","Range","Minimum","Maximum","Sum","Count"]
        for index in range(len(stats1)):
            self.stats_table.setItem(index,0,QTableWidgetItem(stats1[index]))
           
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.stats_table)
            
        self.setLayout(v_layout)
        self.setWindowTitle('Daniel Moses: Assignment 1 \n Introduction to Descriptive Statistics')
        self.activateWindow()
        self.raise_()
        self.show()
    
    def load_data(self):        
       #for this example, we'll hard code the file name.
       #chicken = self.QFileDialog.selectFile()
       #print(chicken)
       print('printing...\n')
       data_file_name = QFileDialog.getOpenFileName(self,'open file')
       #print(data_file_name[0])
       #data_file_name = "Historical Temperatures from Moose Wyoming.csv"
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
        stdv_value = np.std(data_array)
        median_value = np.median(data_array)
        variance = np.var(data_array)
        kurt = stats.kurtosis(data_array, axis =0, fisher =True, bias = True)
        skew = stats.skew(data_array, bias = True)
        standard_err = stats.sem(data_array, axis =0)
        min_val = min(data_array)
        max_val = max(data_array)
        range_val = max_val-min_val
        mode = statistics.mode(data_array)
        count = len(data_array)
        summ = sum(data_array)
        
        #stat_format =QTableWidgetItem("{:.3f}".format(stat_value))
        stats_values = [mean_value,standard_err,median_value,mode,stdv_value,variance,kurt,skew,
                        range_val,min_val,max_val,summ,count]
        
        for index in range(len(stats_values)):
                self.stats_table.setItem(index,1,QTableWidgetItem("{:.3f}".format(stats_values[index])))
            
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