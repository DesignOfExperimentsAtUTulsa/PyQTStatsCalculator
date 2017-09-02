#!/bin/env/python
# An introduction sample source code for some basic statistics

#Import 
import sys
from PyQt5.QtWidgets import  (QWidget, QTreeView, QMessageBox, QHBoxLayout, QMainWindow,
                             QFileDialog, QLabel, QSlider, QCheckBox, QApplication,
                             QLineEdit, QVBoxLayout, QApplication, QPushButton,
                             QTableWidget, QTableWidgetItem,QSizePolicy, QTextEdit,
                             QGridLayout,QGroupBox, QAction, QMenu)
from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QIcon

import numpy as np
from scipy import stats
import statistics, math

class StatCalculator(QWidget):

    def __init__(self):
        super().__init__()

        # Upon startup, run a user interface routine
        self.init_ui()
              

    def init_ui(self):
        #Builds GUI
        self.setGeometry(200,200,800,800)

        # Load Button
        self.load_button = QPushButton('Load Data', self)
        self.load_button.clicked.connect(self.openFileNameDialog)
        
        # Check box select all
        self.all_checkbox = QCheckBox('Select all', self)
        self.all_checkbox.stateChanged.connect(self.selectall)
        
        # Check box of statisticsx
        self.mean_checkbox = QCheckBox('Mean',self)
        self.mean_checkbox.stateChanged.connect(self.compute_stats)

        self.stderr_checkbox = QCheckBox('Standard Error',self)
        self.stderr_checkbox.stateChanged.connect(self.compute_stats)

        self.median_checkbox = QCheckBox('Median',self)
        self.median_checkbox.stateChanged.connect(self.compute_stats)

        self.mode_checkbox = QCheckBox('Mode',self)
        self.mode_checkbox.stateChanged.connect(self.compute_stats)

        self.std_checkbox = QCheckBox('Std Dev',self)
        self.std_checkbox.stateChanged.connect(self.compute_stats)

        self.variance_checkbox = QCheckBox('Variance',self)
        self.variance_checkbox.stateChanged.connect(self.compute_stats)

        self.kurt_checkbox = QCheckBox('Kurtosis', self)
        self.kurt_checkbox.stateChanged.connect(self.compute_stats)

        self.skew_checkbox = QCheckBox('Skewness', self)
        self.skew_checkbox.stateChanged.connect(self.compute_stats)

        self.range_checkbox = QCheckBox('Range',self)
        self.range_checkbox.stateChanged.connect(self.compute_stats)

        self.min_checkbox = QCheckBox('Min',self)
        self.min_checkbox.stateChanged.connect(self.compute_stats)

        self.max_checkbox = QCheckBox('Max',self)
        self.max_checkbox.stateChanged.connect(self.compute_stats)

        self.sum_checkbox = QCheckBox('Sum',self)
        self.sum_checkbox.stateChanged.connect(self.compute_stats)

        # Initial output        
        self.mean_label = QLabel("Mean checkbox not selected",self)
        self.stderr_label = QLabel("Standar error checkbox not selected",self)
        self.median_label = QLabel("Median checkbox not selected",self)
        self.mode_label = QLabel("Mode checkbox not selected",self)
        self.stdev_label =  QLabel("Std Dev checkbox not selected",self)
        self.variance_label = QLabel("Variance checkbox not selected",self)
        self.kur_label = QLabel("Kurtosis checkbox not selected",self)
        self.skew_label = QLabel("Skewness checkbox not selected",self)
        self.range_label = QLabel("Rangge checkbox not selected",self)
        self.min_label = QLabel("Min checkbox not selected", self)
        self.max_label = QLabel("Max checkbox not selected", self)
        self.sum_label = QLabel("Sum checkbox not selected", self)
        
        #Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)

    # BOX TO GROUP BUTTONS & TABLE
        table_box = QGroupBox("Data")
        
        table_box_layout = QVBoxLayout()
        
        table_box_layout.addWidget(self.load_button)
        table_box_layout.addWidget(self.data_table)
        
        table_box.setLayout(table_box_layout)

    # BOX TO GROUP THE CHECHBOXES
        selc_stats_box = QGroupBox("Select statistics parameters to show")

        selc_stats_box_layout = QGridLayout()
        selc_stats_box_layout.addWidget(self.mean_checkbox,0,0)
        selc_stats_box_layout.addWidget(self.stderr_checkbox,0,1)
        selc_stats_box_layout.addWidget(self.median_checkbox,0,2)
        selc_stats_box_layout.addWidget(self.mode_checkbox,0,3)
        selc_stats_box_layout.addWidget(self.std_checkbox,1,0)
        selc_stats_box_layout.addWidget(self.variance_checkbox,1,1)
        selc_stats_box_layout.addWidget(self.kurt_checkbox,1,2)
        selc_stats_box_layout.addWidget(self.skew_checkbox,1,3)
        selc_stats_box_layout.addWidget(self.range_checkbox,2,0)
        selc_stats_box_layout.addWidget(self.min_checkbox,2,1)
        selc_stats_box_layout.addWidget(self.max_checkbox,2,2)
        selc_stats_box_layout.addWidget(self.sum_checkbox,2,3)
        selc_stats_box_layout.addWidget(self.all_checkbox,3,0)
                
        selc_stats_box.setLayout(selc_stats_box_layout)

    # LEFT HAND SIDE BOX
        left_box = QGroupBox()
        
        left_box_layout = QVBoxLayout()
        left_box_layout.addWidget(table_box)
        left_box_layout.addWidget(selc_stats_box)

        left_box.setLayout(left_box_layout)

    # RESULTS PRINT BOX
        rigth_box = QGroupBox()

        rigth_box_layout = QVBoxLayout()
        rigth_box_layout.addWidget(self.mean_label)
        rigth_box_layout.addWidget(self.stderr_label)
        rigth_box_layout.addWidget(self.median_label)
        rigth_box_layout.addWidget(self.mode_label)
        rigth_box_layout.addWidget(self.stdev_label)
        rigth_box_layout.addWidget(self.variance_label)
        rigth_box_layout.addWidget(self.kur_label)
        rigth_box_layout.addWidget(self.skew_label)
        rigth_box_layout.addWidget(self.range_label)
        rigth_box_layout.addWidget(self.min_label)
        rigth_box_layout.addWidget(self.max_label)
        rigth_box_layout.addWidget(self.sum_label)

        rigth_box.setLayout(rigth_box_layout)

    # GUI LAYOUT
        v_layout = QGridLayout()
        v_layout.addWidget(left_box,0,0)
        v_layout.addWidget(rigth_box,0,1)

        self.setLayout(v_layout)

        self.setWindowTitle('Jorge Lopez. HW1')
        self.activateWindow()
        self.raise_()
        self.show()
        
    def selectall(self):
        if self.mean_checkbox.isChecked():  
            self.mean_checkbox.setChecked(True)          
        else:
            self.mean_checkbox.setChecked(True)

        if self.stderr_checkbox.isChecked():  
            self.stderr_checkbox.setChecked(True)          
        else:
            self.stderr_checkbox.setChecked(True)

        if self.median_checkbox.isChecked():  
            self.median_checkbox.setChecked(True)          
        else:
            self.median_checkbox.setChecked(True)

        if self.mode_checkbox.isChecked():  
            self.mode_checkbox.setChecked(True)          
        else:
            self.mode_checkbox.setChecked(True)

        if self.std_checkbox.isChecked():  
            self.std_checkbox.setChecked(True)          
        else:
            self.std_checkbox.setChecked(True)

        if self.variance_checkbox.isChecked():  
            self.variance_checkbox.setChecked(True)          
        else:
            self.variance_checkbox.setChecked(True)

        if self.kurt_checkbox.isChecked():  
            self.kurt_checkbox.setChecked(True)          
        else:
            self.kurt_checkbox.setChecked(True)

        if self.skew_checkbox.isChecked():  
            self.skew_checkbox.setChecked(True)          
        else:
            self.skew_checkbox.setChecked(True)

        if self.range_checkbox.isChecked():  
            self.range_checkbox.setChecked(True)          
        else:
            self.range_checkbox.setChecked(True)

        if self.min_checkbox.isChecked():  
            self.min_checkbox.setChecked(True)          
        else:
            self.min_checkbox.setChecked(True)

        if self.max_checkbox.isChecked():  
            self.max_checkbox.setChecked(True)          
        else:
            self.max_checkbox.setChecked(True)

        if self.sum_checkbox.isChecked():  
            self.sum_checkbox.setChecked(True)          
        else:
            self.sum_checkbox.setChecked(True)            
     
        
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"file to open", "", "CSV (*.csv)", options=options)
        if fileName:
            print(fileName)
            self.load_data(fileName)
            #self.data_name = fileName
        
        
    
    def load_data(self,fileName):        
       #for this example, we'll hard code the file name.
       data_file_name = fileName
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
        stderr_value = stats.sem(data_array)
        median_value = np.median(data_array)
        stdev_value = np.std(data_array)
        mode_a = []
        mode_a = stats.mode(data_array)
        mode_a2 = np.array(mode_a)
        mode_value = mode_a2[0]
        variance_value = np.var(data_array)
        kurt_value = stats.kurtosis(data_array)
        skew_value = stats.skew(data_array)
        range_value = np.max(data_array) - np.min(data_array)
        min_value = np.min(data_array)
        max_value = np.max(data_array)
        sum_value = np.sum(data_array)
        
     
        print("Mean = {0:5f}".format(mean_value))

        if self.mean_checkbox.isChecked():
            self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
        else:
            self.mean_label.setText("Mean checkbox not selected")    
            
        if self.stderr_checkbox.isChecked():
            self.stderr_label.setText("Standard Error = {:0.3f}".format(stderr_value))
        else:
            self.stderr_label.setText("Standar error checkbox not selected")
            
        if self.median_checkbox.isChecked():
            self.median_label.setText("Median = {:0.3f}".format(median_value))
        else:
            self.median_label.setText("Median checkbox not selected")                  

        if self.mode_checkbox.isChecked():
            self.mode_label.setText("Mode = {:0.3f}".format(mode_value[0]))
        else:
            self.mode_label.setText("Mode checkbox not selected")

        if self.std_checkbox.isChecked():
            self.stdev_label.setText("STD = {:0.3f}".format(stdev_value))
        else:
            self.stdev_label.setText("Std Dev checkbox not selected")
            
        if self.variance_checkbox.isChecked():
            self.variance_label.setText("Variance = {:0.3f}".format(variance_value))
        else:
            self.variance_label.setText("Variance checkbox not selected")

        if self.kurt_checkbox.isChecked():
            self.kur_label.setText("Kurtosis = {:0.3f}".format(kurt_value))
        else:
            self.kur_label.setText("Kurtosis checkbox not selected")
            
        if self.skew_checkbox.isChecked():
            self.skew_label.setText("Skewness = {:0.3f}".format(skew_value))
        else:
            self.skew_label.setText("Skewness checkbox not selected")
            
        if self.range_checkbox.isChecked():
            self.range_label.setText("Range = {:0.3f}".format(range_value))
        else:
            self.range_label.setText("Rangge checkbox not selected")
            
        if self.min_checkbox.isChecked():
            self.min_label.setText("Min = {:0.3f}".format(min_value))
        else:
            self.min_label.setText("Min checkbox not selected")

        if self.max_checkbox.isChecked():
            self.max_label.setText("Max = {:0.3f}".format(max_value))
        else:
            self.max_label.setText("Max checkbox not selected")
            
        if self.sum_checkbox.isChecked():
            self.sum_label.setText("Sum = {:0.3f}".format(sum_value))
        else:
            self.sum_label.setText("Sum checkbox not selected")

if __name__ == '__main__':
    #Start the program this way according to https://stackoverflow.com/questions/40094086/python-kernel-dies-for-second-run-of-pyqt5-gui
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    execute = StatCalculator()
    sys.exit(app.exec_())
