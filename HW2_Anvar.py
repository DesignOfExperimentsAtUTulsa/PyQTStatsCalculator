# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 19:09:49 2017

@author: Anvar
"""

import sys
from PyQt5.QtCore import QCoreApplication, Qt, QModelIndex
from PyQt5.QtGui import *
from PyQt5.QtGui import (QIcon,QIntValidator)
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, 
                            QTableWidget, QGridLayout, QTableWidgetItem, QGroupBox, QHBoxLayout,
                            QVBoxLayout, QLabel, QSizePolicy, QCheckBox, QInputDialog, 
                            QMessageBox, QAbstractButton, QSlider, QLineEdit)
import numpy as np
from scipy.stats import (norm,lognorm,expon,t,chi2,f)

import os
 
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.mlab as mlab

rcParams.update({'figure.autolayout': True})

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        FigureCanvas.mpl_connect(self,'button_press_event', self.export)
        
    def export(self,event):
        if event.dblclick:
            filename = "ExportedGraph.pdf"
            self.fig.savefig(filename)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Saved a copy of the graphics window to {}".format(filename))
            msg.setWindowTitle("Saved PDF File")
            msg.setDetailedText("The full path of the file is \n{}".format(os.path.abspath(os.getcwd())))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowModality(Qt.ApplicationModal)
            msg.exec_()
            print("Exported PDF file")
        
class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.axes.set_xlabel("X Label")
        self.axes.set_ylabel("Y Label")
        self.axes.set_title("Title")
        self.axes.grid(True)
             
    def plot_histogram(self,data_array,bin_num,legend_label,data_label="Temperature",
                       title="Probability Density Function Plots"):
        self.axes.cla() 
        self.axes.hist(data_array,bins=bin_num,
                       normed=True,label=legend_label,
                       edgecolor='b',color='y')
        self.axes.set_xlabel(data_label)
        self.axes.set_ylabel("Estimated Prob. Density Funct.")
        self.axes.set_title(title)
        self.axes.legend(loc=0,shadow=True)
        self.axes.grid(True)
        self.draw()
        print("Finished Drawing Normalized Histogram.")
        
          
    def plot_random_variable(self,data,rv,df,df2):
        data_mean = np.mean(data)
        data_sigma = np.std(data)
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(xmin,xmax, 100) #x = np.linspace(loc-3*scale,loc+3*scale, 100)
        
        if rv.name =='lognorm':
          s = np.sqrt(np.log(1+data_sigma**2/data_mean**2))
          y = rv.pdf(x,s,loc=0,scale=data_sigma)
        elif rv.name =='norm':
          y = rv.pdf(x,loc=data_mean,scale=data_sigma)
        elif rv.name =='expon':
          y = rv.pdf(x,loc=0,scale=data_sigma)
        elif rv.name =='t':
          df = 2*data_sigma**2/(data_sigma**2-1)
          y = rv.pdf(x,df,loc=data_mean,scale=data_sigma)
        elif rv.name =='chi2':
          chi2_df = df
          y = rv.pdf(x,chi2_df,loc=0)#,scale=data_sigma)
        elif rv.name =='f':
          dfn = df
          dfd = df2
          y = rv.pdf(x,dfn,dfd,loc=0,scale=data_sigma)
           
        self.axes.plot(x,y,label=rv.name)
        self.axes.legend(loc=0,shadow=True)
        self.draw()
   
class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle('Stats_Graph_Anvar Akhiiartdinov')
        
        extractAction = QAction('&Exit', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('leave the app')
        extractAction.triggered.connect(self.close_application)
        
        extractAction1 = QAction('&Open .CSV', self)
        extractAction1.setShortcut('Ctrl+O')
        extractAction1.setStatusTip('Open .CSV file')
        extractAction1.triggered.connect(self.open_file)
        
        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction1)
        fileMenu.addAction(extractAction)
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.graph_canvas = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
                                    
        self.data_table = QTableWidget(self.main_widget)  
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        table_box = QGroupBox("Data Table")
        table_box_layout = QVBoxLayout()
        table_box_layout.addWidget(self.data_table)
        table_box.setLayout(table_box_layout)
                     
        self.mean_label = QLabel("Mean: Not Computed Yet", self.main_widget)
        self.std_label = QLabel("Std Dev: Not Computed Yet", self.main_widget)
        stats_box = QGroupBox("Summary Statistics")
        stats_box_layout = QVBoxLayout()
        stats_box_layout.addWidget(self.mean_label)
        stats_box_layout.addWidget(self.std_label)
        stats_box.setLayout(stats_box_layout)
        
        self.bin_slider = QSlider(self.main_widget)
        self.bin_slider.setRange(10, 200)
        self.bin_slider.setValue(100)
        self.bin_slider.setTickPosition(QSlider.TicksBelow)
        self.bin_slider.setTickInterval(10)
        self.bin_slider.setOrientation(Qt.Horizontal)
        self.bin_slider.setGeometry(5, 5, 10, 10) 
        self.bin_slider.valueChanged.connect(self.valuechange)
        
        self.bin_label = QLabel("{:0.0f}".format(self.bin_slider.value()), self.main_widget)
        
        self.bin_button = QPushButton("Reset",self.main_widget)
        self.bin_button.clicked.connect(self.compute_stats)
                
        bin_regulator_box = QHBoxLayout()
        bin_regulator_box.addWidget(self.bin_button)
        bin_regulator_box.addWidget(self.bin_slider)
        bin_regulator_box.addWidget(self.bin_label)
        
        canvas_box = QGroupBox("Plotting Area")
        canvas_box_layout = QVBoxLayout()
        canvas_box_layout.addWidget(self.graph_canvas)
        canvas_box_layout.addLayout(bin_regulator_box)
        canvas_box.setLayout(canvas_box_layout)
        
        self.chi2_slider = QSlider(self.main_widget)
        self.chi2_slider.setRange(0, 90)
        self.chi2_slider.setValue(45)
        self.chi2_slider.setTickPosition(QSlider.TicksBelow)
        self.chi2_slider.setTickInterval(5)
        self.chi2_slider.setOrientation(Qt.Horizontal)
        self.chi2_slider.setGeometry(5, 5, 10, 10) 
        self.chi2_slider.valueChanged.connect(self.valuechange)
        
        self.f_slider1 = QSlider(self.main_widget)
        self.f_slider1.setRange(0, 90)
        self.f_slider1.setValue(45)
        self.f_slider1.setTickPosition(QSlider.TicksBelow)
        self.f_slider1.setTickInterval(5)
        self.f_slider1.setOrientation(Qt.Horizontal)
        self.f_slider1.resize(20,20) 
        self.f_slider1.valueChanged.connect(self.valuechange)
        
        self.f_label2_t = QLabel("F DF2", self.main_widget)
        self.f_dfedit = QLineEdit("10",self.main_widget)
        self.f_dfedit.setValidator(QIntValidator())
        self.f_dfedit.setMaxLength(3)
        self.f_dfedit.resize(10,20)
        
        self.chi2_label_t = QLabel("Chi2 DF", self.main_widget)
        self.chi2_label = QLabel("{:0.0f}".format(self.chi2_slider.value()), self.main_widget)
        self.f_label1_t = QLabel("F DF1", self.main_widget)
        self.f_label1 = QLabel("{:0.0f}".format(self.f_slider1.value()), self.main_widget)
        
        self.normal_checkbox = QCheckBox('Normal Distribution',self.main_widget)
        self.normal_checkbox.stateChanged.connect(self.compute_stats)
        self.log_normal_checkbox = QCheckBox('Log-Normal Distribution',self.main_widget)
        self.log_normal_checkbox.stateChanged.connect(self.compute_stats)
        self.exp_checkbox = QCheckBox('Exponential Distribution',self.main_widget)
        self.exp_checkbox.stateChanged.connect(self.compute_stats)
        self.t_checkbox = QCheckBox('T Distribution',self.main_widget)
        self.t_checkbox.stateChanged.connect(self.compute_stats)
        self.chi2_checkbox = QCheckBox('Chi2 Distribution',self.main_widget)
        self.chi2_checkbox.stateChanged.connect(self.compute_stats)
        self.f_checkbox = QCheckBox('F Distribution',self.main_widget)
        self.f_checkbox.stateChanged.connect(self.compute_stats)
        
        distribution_box = QGroupBox("Distribution Functions")
        
        distribution_box_layout_hor_chi = QHBoxLayout()
        distribution_box_layout_hor_chi.addWidget(self.chi2_checkbox)
        distribution_box_layout_hor_chi.addWidget(self.chi2_label_t)
        distribution_box_layout_hor_chi.addWidget(self.chi2_slider)
        distribution_box_layout_hor_chi.addWidget(self.chi2_label)
        
        distribution_box_layout_hor_f = QHBoxLayout()
        distribution_box_layout_hor_f.addWidget(self.f_label1_t)
        distribution_box_layout_hor_f.addWidget(self.f_slider1)
        distribution_box_layout_hor_f.addWidget(self.f_label1)
                                      
        distribution_box_layout_hor_f1 = QHBoxLayout()
        distribution_box_layout_hor_f1.addWidget(self.f_label2_t)
        distribution_box_layout_hor_f1.addWidget(self.f_dfedit)
        
        distribution_box_layout_ver_f = QVBoxLayout()
        distribution_box_layout_ver_f.addLayout(distribution_box_layout_hor_f)
        distribution_box_layout_ver_f.addLayout(distribution_box_layout_hor_f1)
        
        distribution_box_layout_hor_ff = QHBoxLayout()
        distribution_box_layout_hor_ff.addWidget(self.f_checkbox)
        distribution_box_layout_hor_ff.addLayout(distribution_box_layout_ver_f)
             
        distribution_box_layout = QVBoxLayout()
        distribution_box_layout.addWidget(self.normal_checkbox)
        distribution_box_layout.addWidget(self.log_normal_checkbox)
        distribution_box_layout.addWidget(self.exp_checkbox)
        distribution_box_layout.addWidget(self.t_checkbox)
        distribution_box_layout.addLayout(distribution_box_layout_hor_chi)
        distribution_box_layout.addLayout(distribution_box_layout_hor_ff)
        distribution_box.setLayout(distribution_box_layout)
        
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(canvas_box,0,1) 
        grid_layout.addWidget(distribution_box,1,1)
                
        self.main_widget.setLayout(grid_layout)
                
        self.show()
        
    def valuechange(self):
        df_chi2 = self.chi2_slider.value()
        self.chi2_label.setText("{:0.0f}".format(df_chi2))
        df1_f = self.f_slider1.value()
        self.f_label1.setText("{:0.0f}".format(df1_f))
        bin_num = self.bin_slider.value()
        self.bin_label.setText("{:0.0f}".format(bin_num))
        
                        
    def close_application(self):
        print('exit')
        sys.exit()
        
    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file',
                                              'Home/', '*.csv')
       
        print('filename', filename, '\n')
        with open(filename[0],'r') as data_file:
            self.data_lines = data_file.readlines()
           
        print("Opened {}".format(filename[0]))
        print(self.data_lines[1:10])
                
        header_row = 1 
        self.data_table_columns = self.data_lines[header_row].strip().split(',')
        self.data_table.setColumnCount(len(self.data_table_columns))
        self.data_table.setHorizontalHeaderLabels(self.data_table_columns)
        
        current_row = -1
        for row in range(header_row+1, len(self.data_lines)):
            row_values = (self.data_lines[row].strip().split(','))
            current_row +=1
            self.data_table.insertRow(current_row)
            for col in range(len(self.data_table_columns)):
                entry = QTableWidgetItem("{}".format(row_values[col]))
                self.data_table.setItem(current_row,col,entry)
        print("Filled {} rows.".format(row))
        
    def compute_stats(self):
        item_list=[]
        items = self.data_table.selectedItems()
        for item in items:
            try:
                item_list.append(float(item.text()))
            except:
                pass
   
        if len(item_list) > 1: 
            data_array = np.asarray(item_list)
            mean_value = np.mean(data_array)
            stdev_value = np.std(data_array)
            
        print("Mean = {0:5f}".format(mean_value))
        self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
        self.std_label.setText("Std Dev = {:0.4f}".format(stdev_value))
        
        bin_str = self.bin_label.text()
        bin_num = int(bin_str)
        
        self.graph_canvas.plot_histogram(data_array,bin_num,'Temp-Histogram')
        
        if self.normal_checkbox.isChecked():
           self.graph_canvas.plot_random_variable(data_array,norm,1,1)
              
        if self.log_normal_checkbox.isChecked():
           self.graph_canvas.plot_random_variable(data_array,lognorm,1,1)
              
        if self.exp_checkbox.isChecked():
           self.graph_canvas.plot_random_variable(data_array,expon,1,1)
        
        if self.t_checkbox.isChecked():
           self.graph_canvas.plot_random_variable(data_array,t,1,1)
           
        if self.chi2_checkbox.isChecked():
            chi2_df_str = self.chi2_label.text()
            chi2_df_num = int(chi2_df_str)
            self.graph_canvas.plot_random_variable(data_array,chi2,chi2_df_num,1)
            
        if self.f_checkbox.isChecked():
            f_df_str = self.f_label1.text()
            f_df_num = int(f_df_str)
            f_df2_str = self.f_dfedit.text()
            f_df2_num = int(f_df2_str)
            print(f_df2_num)
            self.graph_canvas.plot_random_variable(data_array,f,f_df_num,f_df2_num)
            
          
               
        
    
if __name__ == "__main__":
  
    app = QApplication(sys.argv)
    mw = window()
    mw.show()
    sys.exit(app.exec())