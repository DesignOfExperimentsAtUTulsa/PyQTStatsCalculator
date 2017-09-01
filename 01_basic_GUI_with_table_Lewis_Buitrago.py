#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys 

from PyQt5.QtWidgets import (QWidget, QTreeView, QMessageBox, QHBoxLayout, 
                             QFileDialog, QLabel, QSlider, QCheckBox, 
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem, QInputDialog,)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication

import numpy as np, scipy.stats as st
from scipy import stats
from statistics import mode

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
               
        self.nameLabel1 = QLabel(self)
        self.nameLabel1.setText('Kth Largest:')
        self.line1 = QLineEdit(self)
        
        self.line1.move(425, 195)
        self.line1.resize(50, 25)
        self.nameLabel1.move(315, 195)
               
        self.nameLabel2 = QLabel(self)
        self.nameLabel2.setText('Kth Smallest:')
        self.line2 = QLineEdit(self)
        
        self.line2.move(425, 225)
        self.line2.resize(50, 25)
        self.nameLabel2.move(315, 225)
        
        self.nameLabel3 = QLabel(self)
        self.nameLabel3.setText('Confidence Level %:')
        self.line3 = QLineEdit(self)
        
        self.line3.move(425, 255)
        self.line3.resize(50, 25)
        self.nameLabel3.move(315, 255)
        
        self.mean_label = QLabel("Mean: Not Computed Yet",self)
        self.sem_label = QLabel("Sem: Not Computed Yet",self)
        self.median_label = QLabel("Median: Not Computed Yet",self)
        self.mode_label = QLabel("Mode: Not Computed Yet",self)
        self.stdev_label = QLabel("Stdev: Not Computed Yet",self)
        self.variance_label = QLabel("Variance: Not Computed Yet",self)
        self.kurtosis_label = QLabel("Kurtosis: Not Computed Yet",self)
        self.skewness_label = QLabel("Skewness: Not Computed Yet",self)
        self.range_label = QLabel("Range: Not Computed Yet",self)
        self.min_label = QLabel("Min: Not Computed Yet",self)
        self.max_label = QLabel("Max: Not Computed Yet",self)
        self.sum_label = QLabel("Sum: Not Computed Yet",self)
        self.count_label = QLabel("Count: Not Computed Yet",self)
        self.kthlargest_label = QLabel("Kth Largest: Not Computed Yet",self)
        self.kthsmallest_label = QLabel("Kth Smallest: Not Computed Yet",self)
        self.confidence_label = QLabel("Confidence: Not Computed Yet",self)
      
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        
        #Define where the widgets go in the window        
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.mean_label)
        v_layout.addWidget(self.sem_label)
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
        v_layout.addWidget(self.kthlargest_label)
        v_layout.addWidget(self.kthsmallest_label)
        v_layout.addWidget(self.confidence_label)
        
        self.setLayout(v_layout)
        self.setWindowTitle('Introduction to Descriptive Statistics by Lewis A Buitrago Gomez')
        self.activateWindow()
        self.raise_()
        self.show()
       
    def load_data(self):  
       #Dialog box to pick any CSV file from Button
       options = QFileDialog.Options()
       options |= QFileDialog.DontUseNativeDialog
       data_file_name, _ = QFileDialog.getOpenFileName(self,"Open a CSV File", "","All Files (*);;CSV Files (*.csv)", options=options)
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

        #Mean
        mean_value = np.mean(data_array)
        print("Mean = {0:6f}".format(mean_value))
        self.mean_label.setText("Mean = {:0.6f}".format(mean_value))
        
        #Mode
        mode_array = []
        mode_array = stats.mode(data_array)
        mode_array2=np.array(mode_array)
        #print(mode_array2)
        mode_value = mode_array2[0]
        #print(mode_value)
        print("Mode = {0:6f}".format(mode_value[0]))
        self.mode_label.setText("Mode = {:0.0f}".format(mode_value[0]))
        
        #Median
        median_value = np.median(data_array)
        print("Median = {0:5f}".format(median_value))
        self.median_label.setText("Median = {:0.1f}".format(median_value))
        
        #Min
        min_value = np.min(data_array)
        print("Min = {0:5f}".format(min_value))
        self.min_label.setText("Min = {:0.0f}".format(min_value))
        
        #Max
        max_value = np.max(data_array)
        print("Max = {0:5f}".format(max_value))
        self.max_label.setText("Max = {:0.0f}".format(max_value))
        
        #Range
        range_value = np.ptp(data_array)
        print("Range = {0:5f}".format(range_value))
        self.range_label.setText("Range = {:0.0f}".format(range_value))
        
        #Sum
        sum_value = np.sum(data_array)
        print("Sum = {0:5f}".format(sum_value))
        self.sum_label.setText("Sum = {:0.0f}".format(sum_value))
        
        #Count
        count_value = len(data_array)
        print("Count = {0:5f}".format(count_value))
        self.count_label.setText("Count = {:0.0f}".format(count_value))
        
        #SEM
        sem_value = stats.sem(data_array)
        print("Sem = {0:5f}".format(sem_value))
        self.sem_label.setText("Sem = {:0.6f}".format(sem_value))
        
        #Stdev
        stdev_value = np.std(data_array)
        print("Stdev = {0:5f}".format(stdev_value))
        self.stdev_label.setText("Stdev = {:0.6f}".format(stdev_value))
        
        #Variance
        variance_value = np.var(data_array)
        print("Variance = {0:5f}".format(variance_value))
        self.variance_label.setText("Variance = {:0.6f}".format(variance_value))
        
        #Kurtosis
        kurtosis_value = stats.kurtosis(data_array)
        print("Kurtosis = {0:5f}".format(kurtosis_value))
        self.kurtosis_label.setText("Kurtosis = {:0.6f}".format(kurtosis_value))
        
        #Skewness
        skewness_value = stats.skew(data_array)
        print("Skewness = {0:5f}".format(skewness_value))
        self.skewness_label.setText("Skewness = {:0.6f}".format(skewness_value))
        
        #Confidence Level(95%) - Ask for %Input 
        confid_level = self.line3.text()
        confidence_level = st.t.interval(0.01*(int(confid_level)), len(data_array)-1, loc=np.mean(data_array), scale=st.sem(data_array))
        print("Confidence = {0:5f}".format((confidence_level[1]-confidence_level[0])*0.5))
        self.confidence_label.setText("Confidence = {:0.6f}".format((confidence_level[1]-confidence_level[0])*0.5))
        
        #kth Largest (2nd) - Ask for k-Input large
        kthlargest_array =[]
        kthlargest_array = sorted(data_array)
        kth_larg = self.line1.text()
        kthlargest_value = kthlargest_array[len(kthlargest_array)-int(kth_larg)]
        print("Kthlargest = {0:6f}".format(kthlargest_value))
        self.kthlargest_label.setText("Kthlargest = {:0.0f}".format(kthlargest_value))
        
        #kth Smallest (2nd) - Ask for k-Input small
        kthsmallest_array =[]
        kthsmallest_array = sorted(data_array)
        kth_small = self.line2.text()
        kthsmallest_value = kthsmallest_array[-1+int(kth_small)]
        print("Kthsmallest = {0:6f}".format(kthsmallest_value))
        self.kthsmallest_label.setText("Kthsmallest = {:0.0f}".format(kthsmallest_value))
        
           
if __name__ == '__main__':
    #Start the program this way according to https://stackoverflow.com/questions/40094086/python-kernel-dies-for-second-run-of-pyqt5-gui
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    execute = StatCalculator()
    sys.exit(app.exec_())
