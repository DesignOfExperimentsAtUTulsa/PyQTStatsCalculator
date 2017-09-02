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
from PyQt5 import QtGui, QtCore, QtWidgets
from tkinter import filedialog
from tkinter import *
import subprocess
import tkinter

from scipy import stats
import statistics
import numpy as np #np is a pointer to the numpy library, hence np.fn() calls a numpy subfunction

class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
        
    def init_ui(self):
        
        #Builds GUI
        self.setGeometry(200,200,500,500)
#==============================================================================
#         
#         #menu bar
#         self.menu_bar=QtWidgets.QMenuBar(self)#QtWidgets.QMenuBar.addMenu(topmenu, 'Open')
#         # file menu
#         self.menu_file = QtWidgets.QMenu(self.menu_bar)
#         self.menu_file.setTitle('File')
#         self.menu_bar.addAction(self.menu_file.menuAction())
# 
#         # exit action
#         self.menu_action_exit = QtWidgets.QAction(self)
#         self.menu_action_exit.setText("Exit")
#         self.menu_action_exit.triggered.connect(self.close)
#==============================================================================

        b1 = QWidget()
        self.load_button = QPushButton(b1)
        self.load_button.setText('Load Data')
        self.load_button.clicked.connect(self.simp_load)
        
        b2 = QWidget()
        self.stats_button = QPushButton(b2)
        self.stats_button.setText('Compute Statistics')
        self.stats_button.clicked.connect(self.compute_stats)
        
        b3=QWidget()
        self.file_button=QPushButton(b3, text="Choose File")
        self.file_button.clicked.connect(self.choose_file)#
        
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.median_label = QLabel("Median: Not Computed Yet",self)
        self.mode_label=QLabel("Mode: Not Computed Yet", self)
        self.stdDev_label = QLabel("Standard Deviation: Not Computed Yet",self)
        self.kurt_label=QLabel("Kurtosis: Not Computed Yet",self)
        self.skew_label=QLabel("Skew: Not Computed Yet",self)
        self.minVal_label=QLabel("Minimum: Not Computed Yet",self)
        self.maxVal_label=QLabel("Maximum: Not Computed Yet",self)
        self.range_label = QLabel("Range: Not Computed Yet",self)
        self.sumT_label=QLabel("Sum: Not Computed Yet",self)
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        #v_layout.addWidget(self.menu_bar)
        v_layout.addWidget(self.load_button)
        #v_layout.addWidget(self.stats_button)
        v_layout.addWidget(self.file_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.mean_label)
        v_layout.addWidget(self.median_label)
        v_layout.addWidget(self.mode_label)
        v_layout.addWidget(self.stdDev_label)
        v_layout.addWidget(self.kurt_label)
        v_layout.addWidget(self.skew_label)
        v_layout.addWidget(self.minVal_label)
        v_layout.addWidget(self.maxVal_label)
        v_layout.addWidget(self.range_label)
        v_layout.addWidget(self.sumT_label)
        
        self.setLayout(v_layout)
        self.setWindowTitle('AustinVs Calc: Introduction to Descriptive Statistics')
        self.activateWindow()
        self.raise_()
        self.show()
    
    def simp_load(self):
        self.load_data("Historical Temperatures from Moose Wyoming.csv")
        
    def load_data(self, filename):    
       try:
           self.data_table.setRowCount(0)
       except:
           pass
       #for this example, we'll hard code the file name.
       data_file_name = filename
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
        
    def choose_file(self):
        root = Tk()
        root.wantedfile =  filedialog.askopenfilename(initialdir = "C:\\" ,title = "Select file",filetypes = (("tab delineated",".csv"),("all files","*.*")))
        #subprocess.Popen(r'explorer \select, "C:"')
        try:
            self.load_data(root.wantedfile)
        except:
            pass
    
    def compute_stats(self):
        
        #setup array
        item_list=[]
        items = self.data_table.selectedItems()
        for item in items:
            try:
                item_list.append(float(item.text()))
            except:
                pass
        #print(item_list)
        #print(items)
    
        data_array = np.asarray(item_list)
        mean_value = np.mean(data_array)
        medianVal=np.median(data_array)
        sumT=sum(item_list)
        length=len(item_list)
        minVal=np.amin(data_array)
        maxVal=np.amax(data_array)
        rangeVal=maxVal-minVal
        stdDev=np.std(data_array)
        kurt=stats.kurtosis(data_array)
 #block comment by ctrl+4, uncomment ctrl+1
        skew=stats.skew(data_array)
        try:
            modeVal=statistics.mode(data_array)
        except:
            modeVal=0
            pass
                
        if len(item_list)>2:
            varVal=statistics.variance(item_list)
        else:
            varVal=0
        #first number ,n, in {n:pf} is index of call in format()
        print("Mean = {0:8.6f} \tMedian= {1:8.6f} \tMode{3:4.1f}\tStandardDeviation= {2:8.6f}".format(mean_value, medianVal, stdDev, modeVal))
        print("  Kurtosis= {0:8.6f}\tSkew= {1:8.6f}\tVariance= {2:8.6f}".format(kurt, skew, varVal))
        print("  MinVal= {0:5.1f}\tMaxVal= {1:5.1f} \tRange= {2:5.1f}".format(minVal, maxVal, rangeVal))
        print("  Items Selected:{0:5.0f} with total sum of values:{1:5.0f} ".format(length, sumT))
        
        self.mean_label.setText("Mean = {:0.6f}".format(mean_value))
        self.median_label.setText("Median = {:0.6f}".format(medianVal))
        self.mode_label.setText("Mode = {:0.6f}".format(modeVal))
        self.stdDev_label.setText("StdDev = {:0.6f}".format(stdDev))
        self.kurt_label.setText("Kurtosis= {:0.6f}".format(kurt))
        self.skew_label.setText("Skew= {:0.6f}".format(skew))
        self.minVal_label.setText("Minimum= {:0.1f}".format(minVal))
        self.maxVal_label.setText("Maximum= {:0.1f}".format(maxVal))
        self.range_label.setText("Range = {:0.1f}".format(rangeVal))
        self.sumT_label.setText("Sum= {:0.1f}".format(sumT))
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
