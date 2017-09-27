"""
@author: Anvar Akhiiartdinov
"""

import sys
from PyQt5.QtCore import QCoreApplication, Qt, QModelIndex
from PyQt5.QtGui import *
from PyQt5.QtGui import (QIcon,QIntValidator,QDoubleValidator)
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, 
                            QTableWidget, QGridLayout, QTableWidgetItem, QGroupBox, QHBoxLayout,
                            QVBoxLayout, QLabel, QSizePolicy, QCheckBox, QInputDialog, 
                            QMessageBox, QAbstractButton, QSlider, QLineEdit)
import numpy as np
from scipy import stats

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
          
    def plot_cdf(self,x,y):
        self.axes.clear()
        self.axes.set_xlabel("variable")
        self.axes.set_ylabel("CDF")
        self.axes.set_title("Empirical Cumulative Probability")
        self.axes.plot(x,y,'ro',label='Monte Carlo CDF',markersize=2)
        self.axes.legend(loc=0,shadow=True)
        self.axes.grid(True)        
        self.draw()
   
class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 1000, 800)
        self.setWindowTitle('Monte Carlo Calculator Anvar Akhiiartdinov')
        
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
        
        #Given data
        self.data_table = QTableWidget(self.main_widget)  
        self.data_table.itemChanged.connect(self.compute_stats)
                      
        data_layout = QVBoxLayout()
        data_layout.addWidget(self.data_table)
                
        table_box = QGroupBox("Data Given")
        table_box.setLayout(data_layout)
        
        #Summary of statistics   
        self.mean_sam1_label_dub = QLabel("Mean of Sample", self.main_widget)                
        self.mean_sam1_label = QLabel("Not retrieved", self.main_widget)
        self.std_sam1_label_dub = QLabel("Std of Sample", self.main_widget)   
        self.std_sam1_label = QLabel("Not retrieved", self.main_widget)
        self.var_sam1_label_dub = QLabel("Variance of Sample", self.main_widget)   
        self.var_sam1_label = QLabel("Not retrieved", self.main_widget)
        self.stderr_sam1_label_dub = QLabel("Std Error of Sample", self.main_widget)   
        self.stderr_sam1_label = QLabel("Not retrieved", self.main_widget)
        self.num_sam1_label_dub = QLabel("Num El of Sample", self.main_widget)   
        self.num_sam1_label = QLabel("Not retrieved", self.main_widget)
        
        stats1_layout = QVBoxLayout()
        stats1_layout.addWidget(self.mean_sam1_label_dub)
        stats1_layout.addWidget(self.std_sam1_label_dub)
        stats1_layout.addWidget(self.var_sam1_label_dub)
        stats1_layout.addWidget(self.stderr_sam1_label_dub)
        stats1_layout.addWidget(self.num_sam1_label_dub)
        
        
        stats2_layout = QVBoxLayout()
        stats2_layout.addWidget(self.mean_sam1_label)
        stats2_layout.addWidget(self.std_sam1_label)
        stats2_layout.addWidget(self.var_sam1_label)
        stats2_layout.addWidget(self.stderr_sam1_label)
        stats2_layout.addWidget(self.num_sam1_label)
               
        stats_layout = QHBoxLayout()
        stats_layout.addLayout(stats1_layout)
        stats_layout.addLayout(stats2_layout)
        stats_box = QGroupBox("Summary Statistics")
        stats_box.setLayout(stats_layout)
        
        #Canvas area
        canvas_box = QGroupBox("Plotting Area")
        canvas_box_layout = QVBoxLayout()
        canvas_box_layout.addWidget(self.graph_canvas)
        canvas_box.setLayout(canvas_box_layout)
        
        #Calculation area
        self.calc_button = QPushButton("Calculate", self.main_widget)
        self.calc_button.clicked.connect(self.calculation)
        
        self.siglevel_label_freeze = QLabel("Significance level", self.main_widget)
        self.siglevel_edit = QLineEdit("0.05",self.main_widget)
        self.siglevel_edit.setValidator(QDoubleValidator())
        self.siglevel_edit.setMaxLength(4)
        self.siglevel_edit.resize(10,20)
        
        sig_layout = QHBoxLayout()
        sig_layout.addWidget(self.siglevel_label_freeze)
        sig_layout.addWidget(self.siglevel_edit)
                
        self.t0_label_freeze = QLabel("t-Student", self.main_widget)
        self.t0_label = QLabel("Not calculated", self.main_widget)
        self.lowmean_label_freeze = QLabel("Low mean", self.main_widget)
        self.lowmean_label = QLabel("Not calculated", self.main_widget)
        self.uppermean_label_freeze = QLabel("Upper mean", self.main_widget)
        self.uppermean_label = QLabel("Not calculated", self.main_widget)
        
        self.chi2l_label_freeze = QLabel("Chi2 Left", self.main_widget)
        self.chi2l_label = QLabel("Not calculated", self.main_widget)
        self.maxvar_label_freeze = QLabel("Max variance", self.main_widget)
        self.maxvar_label = QLabel("Not calculated", self.main_widget)
        self.maxstd_label_freeze = QLabel("Max Stddev", self.main_widget)
        self.maxstd_label = QLabel("Not calculated", self.main_widget)
        
        self.mc_lower_label_freeze = QLabel("MC lower bound", self.main_widget)
        self.mc_lower_label = QLabel("Not calculated", self.main_widget)
        self.mc_upper_label_freeze = QLabel("MC upper bound", self.main_widget)
        self.mc_upper_label = QLabel("Not calculated", self.main_widget)
        
        self.st_lower_label_freeze = QLabel("Lower bound from Stat", self.main_widget)
        self.st_lower_label = QLabel("Not calculated", self.main_widget)
        self.st_upper_label_freeze = QLabel("Upper bound from Stat", self.main_widget)
        self.st_upper_label = QLabel("Not calculated", self.main_widget)
               
        mean_freeze_layout = QVBoxLayout()
        mean_freeze_layout.addWidget(self.t0_label_freeze)
        mean_freeze_layout.addWidget(self.lowmean_label_freeze)
        mean_freeze_layout.addWidget(self.uppermean_label_freeze)
        
        mean_layout = QVBoxLayout()
        mean_layout.addWidget(self.t0_label)
        mean_layout.addWidget(self.lowmean_label)
        mean_layout.addWidget(self.uppermean_label)
        
        m_layout = QHBoxLayout()
        m_layout.addLayout(mean_freeze_layout)
        m_layout.addLayout(mean_layout)
        
        mean_box = QGroupBox("CI for the Mean")
        mean_box.setLayout(m_layout)
        
        var_freeze_layout = QVBoxLayout()
        var_freeze_layout.addWidget(self.chi2l_label_freeze)
        var_freeze_layout.addWidget(self.maxvar_label_freeze)
        var_freeze_layout.addWidget(self.maxstd_label_freeze)
        
        var_layout = QVBoxLayout()
        var_layout.addWidget(self.chi2l_label)
        var_layout.addWidget(self.maxvar_label)
        var_layout.addWidget(self.maxstd_label)
        
        v_layout = QHBoxLayout()
        v_layout.addLayout(var_freeze_layout)
        v_layout.addLayout(var_layout)
        
        var_box = QGroupBox("Upper Bound on the Variance")
        var_box.setLayout(v_layout)
                
        mc_freeze_layout = QVBoxLayout()
        mc_freeze_layout.addWidget(self.mc_lower_label_freeze)
        mc_freeze_layout.addWidget(self.mc_upper_label_freeze)
        mc_freeze_layout.addWidget(self.st_lower_label_freeze)
        mc_freeze_layout.addWidget(self.st_upper_label_freeze)
        
        mc_layout = QVBoxLayout()
        mc_layout.addWidget(self.mc_lower_label)
        mc_layout.addWidget(self.mc_upper_label)
        mc_layout.addWidget(self.st_lower_label)
        mc_layout.addWidget(self.st_upper_label)
               
        mcc_layout = QHBoxLayout()
        mcc_layout.addLayout(mc_freeze_layout)
        mcc_layout.addLayout(mc_layout)
        
        mc_box = QGroupBox("Monte Carlo Results")
        mc_box.setLayout(mcc_layout)
                
        ver_layout = QVBoxLayout()
        ver_layout.addWidget(self.calc_button)
        ver_layout.addLayout(sig_layout)
        ver_layout.addWidget(mean_box)
        ver_layout.addWidget(var_box)
        ver_layout.addWidget(mc_box)
        
        calc_box = QGroupBox("Calculation Area")
        calc_box.setLayout(ver_layout)
        
        grid_layout = QGridLayout()
        grid_layout.addWidget(table_box,0,0) 
        grid_layout.addWidget(stats_box,1,0)
        grid_layout.addWidget(canvas_box,0,1) 
        grid_layout.addWidget(calc_box,1,1) 
                
        self.main_widget.setLayout(grid_layout)
                
        self.show()
        
                        
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
                
        header_row = 0 
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
                
        sample1_list=[]
        for row in range(self.data_table.rowCount()):
            sample1_list.append(float(self.data_table.item(row,0).text()))
              
        sam1_array = np.asarray(sample1_list)
        self.mean_sam1 = np.mean(sam1_array)
        self.stdev_sam1 = np.std(sam1_array,ddof=1)
        self.num_sam1 = len(sam1_array)
        self.var_sam1 = self.stdev_sam1**2
        self.stderr_sam1 = self.stdev_sam1 / np.sqrt(self.num_sam1)
            
        self.mean_sam1_label.setText("{:0.5f}".format(self.mean_sam1))
        self.std_sam1_label.setText("{:0.5f}".format(self.stdev_sam1))
        self.var_sam1_label.setText("{:0.5f}".format(self.var_sam1))
        self.stderr_sam1_label.setText("{:0.5f}".format(self.stderr_sam1))
        self.num_sam1_label.setText("{:0.0f}".format(self.num_sam1))
        
            
    def calculation(self):
        
        sig_lev = self.siglevel_edit.text()
        sig_lev = float(sig_lev)
        t_siglev = stats.t.ppf(1-sig_lev/2, self.num_sam1)
        lowmean = self.mean_sam1 - t_siglev*self.stderr_sam1
        uppermean = self.mean_sam1 + t_siglev*self.stderr_sam1
        
        chi2_lower = stats.chi2.ppf(sig_lev, self.num_sam1-1)
        maxvar = (self.num_sam1-1) * self.var_sam1 / chi2_lower
        maxstddev = np.sqrt(maxvar)
        
        self.t0_label.setText("{:0.5f}".format(t_siglev))
        self.lowmean_label.setText("{:0.5f}".format(lowmean))
        self.uppermean_label.setText("{:0.5f}".format(uppermean))
        self.chi2l_label.setText("{:0.5f}".format(chi2_lower))
        self.maxvar_label.setText("{:0.5f}".format(maxvar))
        self.maxstd_label.setText("{:0.5f}".format(maxstddev))
        
        #monte carlo page
        mc_array = np.zeros(10000)
        for i in range(len(mc_array)):
            mc_array[i] = self.mean_sam1 + stats.t.ppf(np.random.random_sample(), self.num_sam1) * \
                          (-1**np.ceil(np.random.random_sample()*2)) * self.stderr_sam1 + \
                          stats.t.ppf(np.random.random_sample(), self.num_sam1-1) * \
                          (-1**np.ceil(np.random.random_sample()*2)) * np.sqrt( (self.num_sam1-1)*self.var_sam1/ \
                          stats.chi2.ppf(np.random.random_sample(), self.num_sam1-1) ) 
                          
        rank_array = stats.rankdata(mc_array, method='ordinal')
        rank_array_c = rank_array/10000
               
        self.graph_canvas.plot_cdf(mc_array,rank_array_c)
        
        index_lower = rank_array.tolist().index(np.round(sig_lev/2*10000))
        index_upper = rank_array.tolist().index(np.round((1-sig_lev/2)*10000))
        lower_bound = mc_array[index_lower]
        upper_bound = mc_array[index_upper]
        
        self.mc_lower_label.setText("{:0.5f}".format(lower_bound))
        self.mc_upper_label.setText("{:0.5f}".format(upper_bound))
        
        lower_bound_st = stats.norm.ppf(sig_lev/2, loc=self.mean_sam1, scale=self.stdev_sam1)
        upper_bound_st = stats.norm.ppf(1-sig_lev/2, loc=self.mean_sam1, scale=self.stdev_sam1)
        
        self.st_lower_label.setText("{:0.5f}".format(lower_bound_st))
        self.st_upper_label.setText("{:0.5f}".format(upper_bound_st))
        
        
    
if __name__ == "__main__":
  
        app = QApplication(sys.argv)
        mw = window()
        mw.show()
        sys.exit(app.exec())