#!/bin/env/python
# An introduction graphing some probability density functions
# 
# Assignment 2 in ME7863: Design and Analysis of Experiments
# Taught By Dr. Jeremy Daily
# Orignially assigned Fall 2017
#
# This is a gentle introduction to programming using Python, numpy, scipy, and PyQt5
# Examples from https://docs.scipy.org/doc/scipy/reference/tutorial/stats.html
# Import modules 
import sys,os
from PyQt5.QtWidgets import (QMainWindow, QWidget,QFileDialog, QLabel, QCheckBox, 
                             QVBoxLayout, QApplication, QPushButton,QTableWidget, 
                             QTableWidgetItem, QGroupBox, QGridLayout, QSizePolicy,
                             QHBoxLayout, QAction,QInputDialog)
from PyQt5.QtCore import QCoreApplication
import numpy as np
from scipy import stats
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import t
from scipy.stats import expon
from scipy.stats import f
from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

#Add a class for matplotlib graphs
# Code was inspired from the Internet
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
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
        filename = "ExportedGraph.pdf"
        self.fig.savefig(filename)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Saved a copy of the graphics window to {}".format(filename))
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Saved PDF File")
        msg.setDetailedText("The full path of the file is \n{}".format(os.path.abspath(os.getcwd())))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowModality(Qt.ApplicationModal)
        msg.exec_()
        print("Exported PDF file")
     
## CLASS OF THE PLOT   
class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself frequently with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.axes.set_xlabel("X Label")
        self.axes.set_ylabel("Y Label")
        self.axes.set_title("Title")
       
#   CREATE AND GRAPH THE HISTOGRAM      
    def plot_histogram(self,data_array, xlabel, ylabel, bins, title, vp):

        self.axes.cla() #Clear axes
        self.axes.hist(data_array,bins=bins,
                       normed=True,label="Data",
                       edgecolor='k',color='y')
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        self.axes.legend(shadow=True)
        self.axes.grid(vp)
            
        self.draw()
        print("Finished Drawing Normalized Histogram.")

#   CALCULATE PDF'S AND PLOTS
    def plot_random_variable(self,data,rv,bins):
        data_mean = np.mean(data)
        data_sigma = np.std(data)
        # data_skew = stats.skew(data)
        xmin,xmax = self.axes.get_xlim()
        x = np.linspace(xmin,xmax, bins)
        
        if rv.name =='lognorm':            
            s = np.sqrt(np.log(1+data_sigma**2/data_mean**2))
            y = rv.pdf(x,s,loc=0,scale=data_sigma)
            m_label = 'Log-Normal'
            
        elif rv.name =='t':            
            shape = data_sigma
            y = rv.pdf(x, df = shape, loc=data_mean, scale = shape)
            m_label = 'Student-T'
            
        elif rv.name == 'expon':
            y = rv.pdf(x,loc=0, scale=data_sigma)
            m_label = 'Exponential'
            
        elif rv.name =='f':
            df1 = 10
            df2 = 10

            y = rv.pdf(x, dfn = df1, dfd = df2, scale = data_sigma)
            m_label = 'F Test'
               
        else:            
            y = rv.pdf(x,loc=data_mean,scale=data_sigma)
            m_label = 'Normal'
          
        self.axes.plot(x,y,label = m_label)
        self.axes.legend(shadow=True)
        self.draw()
  
## CLASS THAT CALCULATE ALL THE STATISTICAL PARAMETERS      
class StatCalculator(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()

    #   Builds GUI
        self.setGeometry(100,70,1800,950)
        self.setWindowTitle('Jorge Lopez. Assigment # 2')

        Load = QAction('Open', self)
        Load.setShortcut('Ctrl+O')
        Load.triggered.connect(self.openFileNameDialog)

        Quit = QAction('Quit', self)
        Quit.setShortcut('Ctrl+Q')
        Quit.triggered.connect(self.close)
        
        Resize = QAction('Resize Window', self)


        self.statusBar()
        menubar = self.menuBar()
        FileOption = menubar.addMenu('File')
        FileOption.addAction(Load)
        FileOption.addAction(Quit)

        WindowOption = menubar.addMenu('Window')
        WindowOption.addAction(Resize)

    # Upon startup, run a user interface routine
        self.init_ui()
              
    def init_ui(self):

        # Add button for second gui
        self.second_gui_button = QPushButton('Statistical Summary',self)
        self.second_gui_button.clicked.connect(self.openSecond)

#        #   Add lables for statistical parameters     
#        # Initial output        
#        self.mean_label = QLabel("Mean checkbox not selected",self)
#        self.stderr_label = QLabel("Standar error checkbox not selected",self)
#        self.median_label = QLabel("Median checkbox not selected",self)
#        self.mode_label = QLabel("Mode checkbox not selected",self)
#        self.stdev_label =  QLabel("Std Dev checkbox not selected",self)
#        self.variance_label = QLabel("Variance checkbox not selected",self)
#        self.kur_label = QLabel("Kurtosis checkbox not selected",self)
#        self.skew_label = QLabel("Skewness checkbox not selected",self)
#        self.range_label = QLabel("Rangge checkbox not selected",self)
#        self.min_label = QLabel("Min checkbox not selected", self)
#        self.max_label = QLabel("Max checkbox not selected", self)
#        self.sum_label = QLabel("Sum checkbox not selected", self)
#
#    #   Add checkboxes
#        # Check box select all
#        self.all_checkbox = QCheckBox('Select all', self)
#        self.all_checkbox.stateChanged.connect(self.selectall)
#
#        # Check box of statistics
#        self.mean_checkbox = QCheckBox('Mean',self)
#        self.mean_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.stderr_checkbox = QCheckBox('Standard Error',self)
#        self.stderr_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.median_checkbox = QCheckBox('Median',self)
#        self.median_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.mode_checkbox = QCheckBox('Mode',self)
#        self.mode_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.std_checkbox = QCheckBox('Std Dev',self)
#        self.std_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.variance_checkbox = QCheckBox('Variance',self)
#        self.variance_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.kurt_checkbox = QCheckBox('Kurtosis', self)
#        self.kurt_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.skew_checkbox = QCheckBox('Skewness', self)
#        self.skew_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.range_checkbox = QCheckBox('Range',self)
#        self.range_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.min_checkbox = QCheckBox('Min',self)
#        self.min_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.max_checkbox = QCheckBox('Max',self)
#        self.max_checkbox.stateChanged.connect(self.compute_stats)
#
#        self.sum_checkbox = QCheckBox('Sum',self)
#        self.sum_checkbox.stateChanged.connect(self.compute_stats)  

    

    #   Set up a Table to display data
        self.data_table = QTableWidget()
        self.data_table.itemSelectionChanged.connect(self.compute_stats)
        main_widget = QWidget()
        self.graph_canvas = MyDynamicMplCanvas(main_widget, width=5, height=4, dpi=100)
      
    #   Histogram adds-on
        self.norhist_checkbox = QCheckBox('Display Grid',self)
        self.norhist_checkbox.stateChanged.connect(self.compute_stats)
        self.hist_button = QPushButton('Histogram Properties',self)
        self.hist_button.clicked.connect(self.histogram_properties)

    #   Box for the the add-on
        addson_box = QGroupBox()
        addson_box_layout = QHBoxLayout()
        addson_box_layout.addWidget(self.norhist_checkbox)
        addson_box_layout.addWidget(self.hist_button)
        addson_box.setLayout(addson_box_layout)    
        
    #   Box for the histogram and the addson of the hitogram
        hist_box = QGroupBox()
        hist_box_layout = QVBoxLayout()
        hist_box_layout.addWidget(self.graph_canvas)
        hist_box_layout.addWidget(addson_box)
        hist_box.setLayout(hist_box_layout) 
        
#    #   Box layout for Statistics print
#        stats_box = QGroupBox("Summary Statistics")
#
#    #   BOX TO GROUP THE CHECHBOXES
#        selc_stats_box = QGroupBox("Select statistics parameters to show")
#        selc_stats_box_layout = QGridLayout()
#        selc_stats_box_layout.addWidget(self.mean_checkbox,0,0)
#        selc_stats_box_layout.addWidget(self.stderr_checkbox,0,1)
#        selc_stats_box_layout.addWidget(self.median_checkbox,0,2)
#        selc_stats_box_layout.addWidget(self.mode_checkbox,0,3)
#        selc_stats_box_layout.addWidget(self.std_checkbox,1,0)
#        selc_stats_box_layout.addWidget(self.variance_checkbox,1,1)
#        selc_stats_box_layout.addWidget(self.kurt_checkbox,1,2)
#        selc_stats_box_layout.addWidget(self.skew_checkbox,1,3)
#        selc_stats_box_layout.addWidget(self.range_checkbox,2,0)
#        selc_stats_box_layout.addWidget(self.min_checkbox,2,1)
#        selc_stats_box_layout.addWidget(self.max_checkbox,2,2)
#        selc_stats_box_layout.addWidget(self.sum_checkbox,2,3)
#        selc_stats_box_layout.addWidget(self.all_checkbox,3,0)
#        selc_stats_box_layout.addWidget(self.second_gui_button,3,1)
#        selc_stats_box.setLayout(selc_stats_box_layout)
#        
#    #   RESULTS PRINT BOX
#        print_box = QGroupBox()
#        print_box_layout = QGridLayout()
#        print_box_layout.addWidget(self.mean_label,0,0)
#        print_box_layout.addWidget(self.stderr_label,0,1)
#        print_box_layout.addWidget(self.median_label,0,2)
#        print_box_layout.addWidget(self.mode_label,1,0)
#        print_box_layout.addWidget(self.stdev_label,1,1)
#        print_box_layout.addWidget(self.variance_label,1,2)
#        print_box_layout.addWidget(self.kur_label,2,0)
#        print_box_layout.addWidget(self.skew_label,2,1)
#        print_box_layout.addWidget(self.range_label,2,2)
#        print_box_layout.addWidget(self.min_label,3,0)
#        print_box_layout.addWidget(self.max_label,3,1)
#        print_box_layout.addWidget(self.sum_label,3,2)
#        print_box.setLayout(print_box_layout)
#
#    #   Box for the statistics   
#        stats_layout = QGridLayout()
#        stats_layout.addWidget(selc_stats_box,0,0) 
#        stats_layout.addWidget(print_box,1,0)
#        stats_box.setLayout(stats_layout)

    #   Create checkboxes for the PDF's
        self.normal_checkbox = QCheckBox('Normal Distribution',self)
        self.normal_checkbox.stateChanged.connect(self.compute_stats)
        
        self.log_normal_checkbox = QCheckBox('Log-Normal Distribution',self)
        self.log_normal_checkbox.stateChanged.connect(self.compute_stats)

        self.expon_checkbox = QCheckBox('Exponential Distribution', self)
        self.expon_checkbox.stateChanged.connect(self.compute_stats)
        
        self.student_checkbox = QCheckBox('Student’s T distribution', self)
        self.student_checkbox.stateChanged.connect(self.compute_stats)
                
        self.f_checkbox = QCheckBox('F distribution',self)
        self.f_checkbox.stateChanged.connect(self.compute_stats)
        
    #   Create box for the PFD's
        distribution_box = QGroupBox("Distribution Functions")
        distribution_box_layout= QGridLayout()
        distribution_box_layout.addWidget(self.normal_checkbox,0,0)
        distribution_box_layout.addWidget(self.log_normal_checkbox,0,1)
        distribution_box_layout.addWidget(self.expon_checkbox,0,2)
        distribution_box_layout.addWidget(self.student_checkbox,1,0)
        distribution_box_layout.addWidget(self.f_checkbox,1,1)
        distribution_box.setLayout(distribution_box_layout)

        #Now we can set all the previously defined boxes into the main window
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.data_table,0,0) 
        grid_layout.addWidget(self.second_gui_button,1,0)
        grid_layout.addWidget(hist_box,0,1) 
        grid_layout.addWidget(distribution_box,1,1)
          
        main_widget.setLayout(grid_layout)
        self.setCentralWidget(main_widget)
        
        self.show()

    def openSecond(self):
        data = self.da
        self.SW = SecondWindow(data)
        self.SW.show()



#   DEFINITINO OF THE SELECT ALL CHECKBOX
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
            
#   DEFINITION FOR THE HISTOGRAM PROPERTIES
    def histogram_properties(self):
        self.bins, okPressed = QInputDialog.getInt(self,
                   "Histogram Properties","Bins number", 28, 0, 300, 200)
        if okPressed:
            print(self.bins)
       
        self.xlabel, ok = QInputDialog.getText(self, 'Histogram Properties', 'X Label')
        if ok:
            print(str(self.xlabel))    
            
        self.ylabel, ok = QInputDialog.getText(self, 'Histogram Properties', 'Y Label')
        if ok:
            print(str(self.ylabel))
            
        self.title, ok = QInputDialog.getText(self, 'Histogram Properties', 'Title')
        if ok:
            print(str(self.title))    
            
        self.graph_canvas.plot_histogram(self.da,self.xlabel,
                                             self.ylabel, self.bins, self.title, self.grid)

        self.compute_stats()
    
#   DEFINITION FOR THE OPN FILE BUTTON 
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"file to open", "", "CSV (*.csv)", options=options)
        if fileName:
            print(fileName)
            self.load_data(fileName)

#   LOAD DATA
    def load_data(self, fileName):        
        #for this example, we'll hard code the file name.
        data_file_name = fileName
        #for the assignment, have a dialog box provide the filename

    #check to see if the file exists and then load it
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

            for row in range(header_row+1, len(self.data_lines)):
               #parse the data in memory into a list 
               row_values = self.data_lines[row].strip().split(',')
               #insert a new row
               current_row = self.data_table.rowCount()
               self.data_table.insertRow(current_row)
               
               #Populate the row with data
               for col in range(len(data_table_columns)):
                   entry = QTableWidgetItem("{}".format(row_values[col]))
                   self.data_table.setItem(current_row,col,entry)
            print("Filled {} rows.".format(row))

            # Inizialization of bins, and histogram properties 
            self.bins = 100;
            self.xlabel = ("Temperature")
            self.ylabel = ("Estimated Prob. Density Funct.")
            self.title = ("Probability Density Function Plots")
            self.grid = True 

#   COMPUTE STATISTICAL PARAMETERS & PDF'S
    def compute_stats(self):
        
        #setup array
        item_list=[]
        items = self.data_table.selectedItems()
        for item in items:
            try:
                item_list.append(float(item.text()))
            except:
                pass
        
        if len(item_list) > 1: #Check to see if there are 2 or more samples
            data_array = np.asarray(item_list)
            self.da = data_array
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
            
        
               

            if self.norhist_checkbox.isChecked():
                self.grid = True
            else:
                self.grid = False
            
            # Histogran plot
            self.graph_canvas.plot_histogram(self.da,self.xlabel, self.ylabel, self.bins, self.title, self.grid)

            if self.normal_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,norm, self.bins)
            if self.log_normal_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,lognorm, self.bins)
            if self.student_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array,t, self.bins)
            if self.expon_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array, expon, self.bins)
            if self.f_checkbox.isChecked():
                self.graph_canvas.plot_random_variable(data_array, f, self.bins)
    
## CLASS THAT CREATE A NEW WINDOW TO SHOW THE STATS
class SecondWindow(QMainWindow):
    def __init__(self, da):
        super(SecondWindow, self).__init__()
        self.setWindowTitle('Stats Summary')
        #self.setGeometry(200,200,500,500)
        #lbl = QLabel('Second Window', self)
        data = da
        self.init_ui(data)
              
    def init_ui(self, data):
        
        #   Add lables for statistical parameters     
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
        
        #   RESULTS PRINT BOX
        print_box = QGroupBox()
        print_box_layout = QVBoxLayout()
        print_box_layout.addWidget(self.mean_label)
        print_box_layout.addWidget(self.stderr_label)
        print_box_layout.addWidget(self.median_label)
        print_box_layout.addWidget(self.mode_label)
        print_box_layout.addWidget(self.stdev_label)
        print_box_layout.addWidget(self.variance_label)
        print_box_layout.addWidget(self.kur_label)
        print_box_layout.addWidget(self.skew_label)
        print_box_layout.addWidget(self.range_label)
        print_box_layout.addWidget(self.min_label)
        print_box_layout.addWidget(self.max_label)
        print_box_layout.addWidget(self.sum_label)
        print_box.setLayout(print_box_layout)

        
        self.setCentralWidget(print_box)
        
        self.stats_calculations(data)
        
    def stats_calculations(self, data):
        
        mean_value = np.mean(data)
        stderr_value = stats.sem(data)
        median_value = np.median(data)
        stdev_value = np.std(data)
        mode_a = []
        mode_a = stats.mode(data)
        mode_a2 = np.array(mode_a)
        mode_value = mode_a2[0]
        variance_value = np.var(data)
        kurt_value = stats.kurtosis(data)
        skew_value = stats.skew(data)
        range_value = np.max(data) - np.min(data)
        min_value = np.min(data)
        max_value = np.max(data)
        sum_value = np.sum(data)
            
    # Check the chebox for statistics status
        self.mean_label.setText("Mean = {:0.3f}".format(mean_value))
        self.stderr_label.setText("Standard Error = {:0.3f}".format(stderr_value))
        self.median_label.setText("Median = {:0.3f}".format(median_value))
        self.mode_label.setText("Mode = {:0.3f}".format(mode_value[0]))
        self.stdev_label.setText("STD = {:0.3f}".format(stdev_value))
        self.variance_label.setText("Variance = {:0.3f}".format(variance_value))
        self.kur_label.setText("Kurtosis = {:0.3f}".format(kurt_value))
        self.skew_label.setText("Skewness = {:0.3f}".format(skew_value))
        self.range_label.setText("Range = {:0.3f}".format(range_value))
        self.min_label.setText("Min = {:0.3f}".format(min_value))
        self.max_label.setText("Max = {:0.3f}".format(max_value))
        self.sum_label.setText("Sum = {:0.3f}".format(sum_value)) 
        
               
        
        
        
        

    



'''       
  1. Add the ability to plot a normalized Histogram of the selected data in the table.
  2. Add a menu option to open a CSV data file.
  3. Add a checkbox for at least 5 distribution functions to plot over the top of the Histogram. 
    a. Include a legend and appropriate labels on your graph.
    b. Include axes labels. (Challenge: make the labels editable in your program).
  4. Use a grid style layout for your GUI
  5. Save the plot to a PDF when you double click on it.
  6. Try to find one of the most obscure distributions as one of your 5. Please try to be different than everyone else. 
  7. Print and turn in a screenshot of your GUI on one page. Be sure your name in in the window title.
  8. Print and turn in the PDF file of the properly labeled Histogram with 2 distributions shown.
'''

if __name__ == '__main__':
    #Start the program this way according to https://stackoverflow.com/questions/40094086/python-kernel-dies-for-second-run-of-pyqt5-gui
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    execute = StatCalculator()
    sys.exit(app.exec_())
