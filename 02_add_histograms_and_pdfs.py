import sys
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, 
							QApplication, QMainWindow, QToolTip, QTableWidget, QTableWidgetItem,
							QGroupBox, QCheckBox, QGridLayout, QSizePolicy, QAction, QFileDialog, QInputDialog,
							QLineEdit, QMessageBox, QSlider)
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QFont
import subprocess, os
import numpy as np
import statistics, math
from scipy import stats #only currently works with winPython cmd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.mlab as mlab
import math



class PlotCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100): 
		self.fig = Figure(figsize=(width,height), dpi=dpi) #creates figure object
		self.axes = self.fig.add_subplot(111) #1 by 1 grid 1st subplot, change if multiple subplots needed

		FigureCanvas.__init__(self, self.fig) #creates FigureCanvas object taking the created figure
		self.setParent(parent) #sets parent of current object

		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding) #allows to expand in X and Y?
		FigureCanvas.updateGeometry(self) #updates geom accordingly?
		FigureCanvas.mpl_connect(self,'button_press_event', self.export) #if figure clicked, calls the export function

		self.graphTitle = "Title" #sets default title
		self.xAxisLabel = "X Axis" #sets default x-axis title
		self.yAxisLabel = "Y Axis" #sets default y-axis title
		self.numOfHistoBins = 50 #sets default number of histograms bins
		self.startingUp = True #current boolean fix to keep slider from setting number of bins before selecting data

	def export(self,event): #saving graphs to pdf
		filename, submit = QInputDialog.getText(self, "Save As", "File Name") #takes name of file to save as
		filename += ".pdf" #uses pdf format for entered filename
		if submit: #if clicked
			self.fig.savefig(filename) #save it as that pdf
			msg = QMessageBox() #creates message box
			msg.setIcon(QMessageBox.Information) #makes information type of icon?
			msg.setText("Saved a copy of the graphics window to {}".format(filename)) #prints name file is saved as
			msg.setWindowTitle("Saved PDF File")
			msg.setDetailedText("The full path of the file is \n{}".format(os.path.abspath(os.getcwd()))) #prints path where saved
			msg.setStandardButtons(QMessageBox.Ok) #makes ok button?
			msg.setWindowModality(Qt.ApplicationModal)#sets dialog box to type that blocks input to other visible windows in same app
			msg.exec_() #escaping dialog box?
			print("Exported PDF file")

	def plotHistogram(self, dataArray): #plots the histogram
		self.currentData = dataArray #sets current data as variable
		self.axes.cla() #clears axes
		self.axes.hist(self.currentData, self.numOfHistoBins, normed=True, Label="Empirical",edgecolor='b',color='y') #makes normalized histogram
		self.axes.set_xlabel(self.xAxisLabel) #sets x axis label
		self.axes.set_ylabel(self.yAxisLabel) #sets y axis label
		self.axes.set_title(self.graphTitle) #sets graph title
		self.axes.legend(shadow=True) #shows legend
		self.draw() #draws graph
		print("Finished Drawing Normalized Histogram.")

	def plotNormal(self, mu, sigma): #plots the normal distribution of the current selected data
		xmin, xmax = self.axes.get_xlim() #stores current x-axis limits
		x = np.linspace(mu-3*sigma, mu+3*sigma, 100) #stores evenly spaced numbers over specified interval
		#for this case, 100 evenly spaces points for 99.7% probability
		y = mlab.normpdf(x, mu, sigma) #stores pdf for each x given mu and sigma
		#yList = y.tolist()
		#myList = self.getNormalDist(x, mu, sigma)
		#self.checkResults(yList, myList)
		self.axes.plot(x,y,label="Normal") #prepares each point for the plot
		self.axes.legend(shadow=True) #shows this plot on the legend
		self.draw() #draws it on the graph
		print("Finished Drawing Normal Distribution")

	"""def checkResults(self, libraryCalcs, myCalcs):
		print("YEA")
		for i in range(len(myCalcs)):
			difference = libraryCalcs[i] - myCalcs[i]
			if(difference <= sys.float_info.epsilon and difference >= -sys.float_info.epsilon):
				print("SAME")
				pass
			else:
				print("They're not equal")

	def getNormalDist(self,x, mu, sigma): #function to check math for std distribution
		valueList = []
		#formula page 157 stat book = Probability and Statistics for Engineering and the Sciences 9th ed. Jay Devore
		frontTerm = 1./(math.sqrt(2* math.pi) * sigma)
		xList = x.tolist() 
		for value in xList:
			numer = (value- mu)**2
			denom = 2*(sigma**2)
			powerTerm = -numer/denom
			eTerm = math.exp(powerTerm)
			valueList.append(frontTerm*eTerm)
		return valueList
	"""
	def plotLogNormal(self, mu, sigma): #verified
		xmin, xmax = self.axes.get_xlim()
		x = np.linspace(mu-3*sigma, mu+3*sigma, 100)
		scale = np.exp(mu)
		shift = 0
		y = stats.lognorm.pdf(x, sigma, shift, scale)
		#yList = y.tolist()
		#myList = self.getLogNormal(x, mu, sigma)
		#self.checkResults(yList, myList)
		self.axes.plot(x,y,label="Log-Normal")
		self.axes.legend(shadow=True)
		self.draw()
		print("Finished Drawing Log-Normal Distribution")

	"""def getLogNormal(self, x, mu, sigma):
		#page 179
		#exponent1 = oldMu + (oldSigma**2)/2
		#exponent2 = 2*oldMu + oldSigma**2
		#mu = math.exp(exponent1)
		#sigma = math.exp(exponent2)
		valueList = []
		xList = x.tolist()
		for value in xList:
			if value < 0:
				valueList.append(0.)
			else:
				frontTerm = 1/(math.sqrt(2*math.pi) * sigma * value)
				numer = (math.log(value) - mu)**2
				denom = 2*(sigma**2)
				powerTerm = -numer/denom
				eTerm = math.exp(powerTerm)
				valueList.append(frontTerm*eTerm)
		return valueList
	"""
	def plotChiSquared(self, mu, sigma, df):
		xmin, xmax = self.axes.get_xlim()
		x = np.linspace(mu-3*sigma, mu+3*sigma, 100)
		y = stats.chi2.pdf(x,df)
		self.axes.plot(x,y,label="Chi-Squared")
		self.axes.legend(shadow=True)
		self.draw()
		print("Finished Drawing Chi-Squared Distribution")

	def plotBeta(self, mu, sigma, alpha, beta):
		xmin, xmax = self.axes.get_xlim()
		x = np.linspace(mu-3*sigma, mu+3*sigma, 100)
		y = stats.beta.pdf(x,alpha,beta)
		self.axes.plot(x,y,label="Beta")
		self.axes.legend(shadow=True)
		self.draw()
		print("Finished Drawing Beta Distribution")

	def plotAlpha(self, mu, sigma, alpha):
		xmin, xmax = self.axes.get_xlim()
		x = np.linspace(mu-3*sigma, mu+3*sigma, 100)
		y = stats.alpha.pdf(x,alpha)
		self.axes.plot(x,y,label="Alpha")
		self.axes.legend(shadow=True)
		self.draw()
		print("Finished Drawing Alpha Distribution")

	def editingGraphTitles(self): #edits axis titles and graph title of graph
		#improving this would be making it one dialog
		#global X_AXIS_LABEL, Y_AXIS_LABEL, GRAPH_TITLE
		title, submit = QInputDialog.getText(self, 'Input Dialog', 'Plot Title:')
		xLabel, submit = QInputDialog.getText(self, 'Input Dialog','X-Axis Label:')
		yLabel, submit = QInputDialog.getText(self, 'Input Dialog','Y-Axis Label:')
		if submit:
			self.graphTitle = title #sets instance vars to entered info
			self.xAxisLabel = xLabel
			self.yAxisLabel = yLabel
			self.plotHistogram(self.currentData) #replots same data with new titles
			print("Success")

	def setNumOfHistoBins(self, sliderValue): #sets number of histogram bins
		self.numOfHistoBins = sliderValue #sets instance variable to value of slider
		print("Bins: " + str(self.numOfHistoBins))
		if not self.startingUp: #fix later. crashes at first run
			self.plotHistogram(self.currentData) #plots same data with new num of histograms
		self.startingUp = False #it's not the first run anymore

class StatMagic (QMainWindow):
	def __init__(self):
		super().__init__() #calls widget constructor
		self.setAcceptDrops(True) #accept dropping files
		self.initUI() #set specific widget details up for our object (the UI)

	def initUI(self): #defining my GUI object
		self.setWindowTitle("Blake Fusick Statistic Calc") #Changes window title
		self.dataTable = QTableWidget() #create data table
		self.dataTable.itemSelectionChanged.connect(self.computeStats) #if selected item is different call computeStats method
		#compute stats in real time as selections are made

		openFile = QAction(QIcon('Open-icon.png'),'Open', self) #creates an action called open file
		openFile.setShortcut('Ctrl+O') #sets ctrl+o as shortcut
		openFile.setStatusTip('Open new File') #sets tip to say what action does
		openFile.triggered.connect(self.openingFile) #calls function openingFile if action called

		menubar = self.menuBar() #adds a menu bar
		fileMenu = menubar.addMenu('&File') #adds File as a menu option
		fileMenu.addAction(openFile) #adds openFile action under File option

		self.graph = PlotCanvas(self, width=5, height=4) #creates object from PlotCanvas
		self.graph.move(0,0) #sets position?
		self.degreesOfFreedom = 1 #dof variable for chi2 distribution
		self.alphaAlpha = 1 #alpha variable for alpha distribution
		self.alphaBeta = 1 #alpha variable for beta distribution
		self.beta = 1 #beta variable for beta distribution
		self.createButtons() #creates buttons from self-made method
		self.createLabels() #creates labels for stat calcs in self-made method
		self.createCheckboxes() #creates checkboxes
		self.createSliders() #creats slides
		self.organizeLayout() #organizes layout of window
		self.setCentralWidget(self.entireLayout) #sets the entire layout as my central widget for QMainWindow
		self.resize(1300,1000) #sizes the window
		self.activateWindow() #inherited from QWidget
		self.setWindowIcon(QIcon('pokecoin.png')) #sets tiny icon on window
		self.show() #shows the GUI

	def editingAlpha(self): #changes alpha variable with entered value for alpha distribution
		alpha, submit = QInputDialog.getText(self, 'Change Variable', 'Alpha') #input dialog box to get alpha
		print(alpha)
		if submit: #when submitting
			self.alphaAlpha = float(alpha) #sets alpha as new var
			self.computeStats() #recomputes stats with new alpha

	def editingBeta(self): #changes alpha and beta variables with given values for beta distribution
		alpha, submit = QInputDialog.getText(self, 'Change Variable', 'Alpha') #input dialog to get alpha
		beta, submit = QInputDialog.getText(self, 'Change Variable', 'Beta') #input dialog to get beta
		print("alpha: " +alpha+ " beta: " + beta)
		if submit:
			self.alphaBeta = float(alpha) #sets instance vars
			self.beta = float(beta)
			self.computeStats() #recomputes/graphs with new alpha/beta

	def editingChi(self): #changes degrees of freedom for chi distribution
		dof, submit = QInputDialog.getText(self, 'Change Variable', 'Degrees of Freedom') #input dialog to get dof
		if submit:
			self.degreesOfFreedom = float(dof) #sets instance var
			self.computeStats() #recomputes with new dof

	def openingFile(self): #opens file via windows dialog
		try: #error handling
			fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/Documents/Fall 2017/Dailys Engr Analysis') #get name of selected file
			with open(fname[0], 'r') as file: #open it as read only
				self.lines = file.readlines() #split into lines
				self.parseData(self.lines) #parse data with custom function
		except: #if error
			pass #do nothing
			 

	def createButtons(self): #creates buttons for GUI
		#global BUTTON_FONT #lets us access the global variable
		buttonFont = QFont("Jokerman", 15)

		self.loadButton = QPushButton('Load Data', self) #create load data button
		self.loadButton.setFont(buttonFont) #set the font
		self.loadButton.setToolTip('Drag and Drop a <b>CSV File</b> on the Window') #make a help popup
		self.loadButton.clicked.connect(self.loadData) #call loadData() if clicked

		self.editTitlesButton = QPushButton('Edit Titles', self) #creates edit titles button
		self.editTitlesButton.clicked.connect(self.graph.editingGraphTitles) #when clicked calls editingGraphTitles function

		self.alphaButton = QPushButton('Alpha Edit Variables', self) #creates alpha edit variables button
		self.alphaButton.clicked.connect(self.editingAlpha) #calls editingAlpha function when clicked

		self.betaButton = QPushButton('Beta Edit Variables', self) #creates beta edit variables button
		self.betaButton.clicked.connect(self.editingBeta) #calls editingBeta function when clicked

		self.chiSquaredButton = QPushButton('Chi-Squared Edit Variables', self) #creates chi2 edit variables button
		self.chiSquaredButton.clicked.connect(self.editingChi) #calls editingChi function when clicked

	def createLabels(self): #creates labels for statistic calculations
		self.labelFont = QFont("Arial Black", 10) #creates label font

		self.meanLabel = QLabel("Mean: Not Computed", self) #default label for mean
		self.stdErrorLabel = QLabel("Standard Error: Not Computed", self) #default label for std error
		self.medianLabel = QLabel("Median: Not Computed", self) #default label for median
		self.modeLabel = QLabel("Mode: Not Computed", self) #default label for mode
		self.stdDeviationLabel = QLabel("Standard Deviation: Not Computed", self) #default label for std deviation
		self.sampleVarianceLabel = QLabel("Sample Variance: Not Computed", self) #default label for sample variance
		self.kurtosisLabel = QLabel("Kurtosis: Not Computed", self) #default label for kurtosis
		self.skewnessLabel = QLabel("Skewness: Not Computed", self) #default label for skewness
		self.rangeLabel = QLabel("Range: Not Computed", self) #default label for range
		self.minimumLabel = QLabel("Minimum: Not Computed", self) #default label for minimum
		self.maximumLabel = QLabel("Maximum: Not Computed", self) #default label for maximum
		self.sumLabel = QLabel("Sum: Not Computed", self) #default label for sum
		self.countLabel = QLabel("Count: Not Computed", self) #default label for count
		self.labels = [self.meanLabel, self.stdErrorLabel, self.medianLabel, self.modeLabel, self.stdDeviationLabel, self.sampleVarianceLabel, self.kurtosisLabel,
					self.skewnessLabel, self. rangeLabel, self.minimumLabel, self.maximumLabel, self.sumLabel, self.countLabel] #put all labels in list
		for label in self.labels:
			label.setFont(self.labelFont) #sets font of all labels

	def createCheckboxes(self): #creates all checkboxes for distributions
		self.normalCheckbox = QCheckBox('Normal Distribution', self) #normal distribution checkbox
		self.logNormalCheckbox = QCheckBox('Log-Normal Distribution', self) #log normal distribution checkbox
		self.alphaCheckbox = QCheckBox('Alpha Distribution', self) #alpha distribution checkbox
		self.betaCheckbox = QCheckBox('Beta Distribution', self) #beta distribution checkbox
		self.chiSquaredCheckbox = QCheckBox('Chi-Squared Distribution', self) #chi2 distribution checkbox
		self.checkboxes = [self.normalCheckbox, self.logNormalCheckbox, self.alphaCheckbox,
							self.betaCheckbox, self.chiSquaredCheckbox]
		for check in self.checkboxes: #for each checkbox
			check.stateChanged.connect(self.computeStats) #if clicked, compute stats
			check.setFont(self.labelFont) #set font to label font

	def createSliders(self): #creates all sliders for GUI
		self.histogramBinSlider = QSlider(Qt.Horizontal, self) #creates slider for number of histogram bins
		self.histogramBinSlider.valueChanged.connect(self.setHistoBins)#if value changed, call setHistoBins
		self.histogramBinSlider.setMinimum(1) #set minimum value of slider
		self.histogramBinSlider.setMaximum(100) #set maximum value of slider
		self.histogramBinSlider.setValue(self.graph.numOfHistoBins) #set value of slider to current value

	def setHistoBins(self): #sets number of histogram bins
		binNumber = self.histogramBinSlider.value() #gets value of the position of slider
		self.graph.setNumOfHistoBins(binNumber) #calls setNumOfHistoBins function from PlotCanvas to change and replot with new bins count

	def organizeLayout(self): #organize widget layout of GUI
		self.entireLayout = QWidget() #create widget to store entire layout
		tableBox = QGroupBox("Data Table") #make data table box
		tableBoxLayout = QVBoxLayout() #create vertical layout
		tableBoxLayout.addWidget(self.loadButton) #add load button 
		tableBoxLayout.addWidget(self.dataTable) #add data table
		tableBox.setLayout(tableBoxLayout) #apply layout to box

		statsBox = QGroupBox("Summary Statistics") #make summary statistics box
		statsBoxLayout = QVBoxLayout() #create vertical layout
		for label in self.labels: #for each label
			label.setAlignment(Qt.AlignCenter) #allign it to the center
			statsBoxLayout.addWidget(label) #add it to the layout
		statsBox.setLayout(statsBoxLayout) #apply layout to the box

		graphBox = QGroupBox("Histogram") #make graph box
		graphBoxLayout = QVBoxLayout() #create vertical layout
		#self.fakeLabel = QLabel("Graph will go here", self) #placeholder
		graphBoxLayout.addWidget(self.graph) #adds graph to box
		graphBoxLayout.addWidget(self.histogramBinSlider)
		graphBoxLayout.addWidget(self.editTitlesButton) #adds edit titles button to box
		graphBox.setLayout(graphBoxLayout) #apply layout to box

		distributionBox = QGroupBox("Distribution Functions") #make dist func box
		distributionBoxLayout = QVBoxLayout() #create vertical layout
		for check in self.checkboxes: #for each checkbox
			distributionBoxLayout.addWidget(check) #add it to layout
		distributionBoxLayout.addWidget(self.alphaButton)
		distributionBoxLayout.addWidget(self.betaButton)
		distributionBoxLayout.addWidget(self.chiSquaredButton)
		distributionBox.setLayout(distributionBoxLayout) #apply layout to box

		gridLayout = QGridLayout() #create grid layout
		#add widgets at the given coordinate
		gridLayout.addWidget(tableBox,0,0)
		gridLayout.addWidget(statsBox,1,0)
		gridLayout.addWidget(graphBox,0,1)
		gridLayout.addWidget(distributionBox,1,1)
		self.entireLayout.setLayout(gridLayout) #set the actual layout so we can see it

	def dragEnterEvent(self,e): #defines what happens when file is dragged into gui
		if e.mimeData().hasUrls(): #issue with csv hasFormat(text/csv)
		#currently if the dragged data has a path
			e.accept() #accept it
		else: #otherwise
			e.ignore() #ignore it
			print("You tried")

	def dropEvent(self, e): #defines what happens when file is dropped into gui
		fileObject = e.mimeData().urls()[0] #stores the file object of the dropped file
		path = fileObject.path() #stores the path of the dropped file
		with open(path[1:]) as file: #opens the file and starts at 1 to strip / from /C:/...
			self.lines = file.readlines() #read the file into lines
		self.parseData(self.lines) #parses data from the lines

	def parseData(self, dataLines): #parses data
		headerRow = 1 #sets which row the header is in
		tableColumns = self.lines[headerRow].strip().split(',') #strip off /n and split on , to find num of columns
		self.dataTable.setColumnCount(len(tableColumns)) #set column count of table to num of columns
		self.dataTable.setHorizontalHeaderLabels(tableColumns) #creates titles of columns

		currentRow = -1 #index for generated table
		for row in range(headerRow + 1, len(self.lines)): #for each row after the header
			rowValues = self.lines[row].strip().split(',') #split them up the same way
			currentRow += 1 #moves on to next row in table we're creating
			self.dataTable.insertRow(currentRow) #insert a row
			for col in range(len(tableColumns)): #for each value in the row
				entry = QTableWidgetItem("{}".format(rowValues[col])) #store it in entry
				self.dataTable.setItem(currentRow,col,entry) #put it in the table
		print("Filled {} rows".format(row)) #prints how many rows were added

	def loadData(self): #just opens file explorer to drag/drop file
		#subprocess.Popen('explorer "{0}"'.format(r'C:\Users\Blake\Documents\Fall 2017\Dailys Engr Analysis'))
		self.openingFile() #new method to actually open file
		#path where to open Windows explorer

	def computeStats(self): #computes all of our statistics and graphs
		itemList = [] #creating list to store data as floats
		items = self.dataTable.selectedItems() #stores currently selected items (objects)
		for item in items: #for each of the items
			try: #error handling
				itemList.append(float(item.text())) #append it to the list as a float
			except: #this way it doesn't crash if no items selected
				pass #do nothing

		dataArray = np.asarray(itemList) #store list as an array
		meanValue = np.mean(dataArray) #find the mean
		medianValue = np.median(dataArray) #find the median
		countValue = len(itemList) #find number of items
		try: #error handling if not enough data is selected for calcs
			modeValue = statistics.mode(itemList) #just returns if single modal
			stdDeviationValue = statistics.stdev(itemList) #sample standard deviation
			sampleVarianceValue = statistics.variance(itemList) #sample variance
			stdErrorValue = stdDeviationValue/math.sqrt(countValue) #std error of mean
			kurtosisValue = stats.kurtosis(dataArray) #stores kurtosis
			skewnessValue = stats.skew(dataArray) #stores skewness
		except: #if error
			pass #do nothing
		minimumValue = np.amin(dataArray) #store the min val
		maximumValue = np.amax(dataArray) #store max val
		rangeValue = maximumValue - minimumValue #store range
		sumValue = sum(itemList) #store sum of items
		#print("Mean = {0:5f}".format(meanValue))
		self.meanLabel.setText("Mean = {:0.3f}".format(meanValue)) #set text for mean
		try: #error handling if no value for calculations like for 1 data point
			#sets text for all the values that need error handling
			self.stdErrorLabel.setText("Standard Error = {:0.3f}".format(stdErrorValue))
			self.modeLabel.setText("Mode = {:0.3f}".format(modeValue))
			self.stdDeviationLabel.setText("Standard Deviation = {:0.3f}".format(stdDeviationValue))
			self.sampleVarianceLabel.setText("Sample Variance = {:0.3f}".format(sampleVarianceValue))
			self.kurtosisLabel.setText("Kurtosis = {:0.3f}".format(kurtosisValue))
			self.skewnessLabel.setText("Skewness = {:0.3f}".format(skewnessValue))
		except: #if error
			#reset the text to None for the those calcs
			self.stdErrorLabel.setText("Standard Error = None")
			self.modeLabel.setText("Mode = None")
			self.stdDeviationLabel.setText("Standard Deviation = None")
			self.sampleVarianceLabel.setText("Sample Variance = None")
			self.kurtosisLabel.setText("Kurtosis = None")
			self.skewnessLabel.setText("Skewness = None")
		#sets text for remainder of stat calcs
		self.medianLabel.setText("Median = {:0.3f}".format(medianValue))
		self.rangeLabel.setText("Range = {:0.3f}".format(rangeValue))
		self.minimumLabel.setText("Minimum = {:0.3f}".format(minimumValue))
		self.maximumLabel.setText("Maximum = {:0.3f}".format(maximumValue))
		self.sumLabel.setText("Sum = {:0.3f}".format(sumValue))
		self.countLabel.setText("Count = {:0.3f}".format(countValue))
		self.graph.plotHistogram(dataArray) #plots the histogram with the data
		if self.normalCheckbox.isChecked(): #if the box is checked
			try:
				self.graph.plotNormal(meanValue, stdDeviationValue) #plots the normal distribution
			except:
				pass
		if self.logNormalCheckbox.isChecked(): #if log normal is checked
			self.graph.plotLogNormal(meanValue, stdDeviationValue) #plots log normal distribution
		if self.alphaCheckbox.isChecked(): #if alpha is checked
			self.graph.plotAlpha(meanValue, stdDeviationValue, self.alphaAlpha) #plots alpha distribution
		if self.betaCheckbox.isChecked(): #if beta is checked
			self.graph.plotBeta(meanValue, stdDeviationValue, self.alphaBeta, self.beta) #plots beta distribution
		if self.chiSquaredCheckbox.isChecked(): #if chi2 is checked
			self.graph.plotChiSquared(meanValue, stdDeviationValue, self.degreesOfFreedom) #plots chi2 distribution

if __name__ == '__main__':
	app = QCoreApplication.instance() #references instance of app if it exists
	if app is None: #keeps it a singleton to prevent kernel from dying?
		app = QApplication(sys.argv)
	window = StatMagic() #creates object we made for the GUI
	sys.exit(app.exec_()) #provides a clean exit for the program so it knows it's