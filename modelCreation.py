# ########################################################################################
# Khuram Chughtai
# Impulse Intelligence
# Web Minning Operations

# The Following are Library expected to exist with standard python install
import os					# Used for OS related Functions generic across all Platforms
import re					# Regex Library used to help parse out words
import json					# Used to Transform data in JSON Format as expected
import sys					# Used to Call System Functions and Import Classes Correctly
import logging 				# Used to Create File Logging Structure that will Help with Debugging
import pandas				# Used to help with parsing data as needed from data files
import requests             # Used to Download Web data and handle headers and act like a browser
import json					# Tools to Handle the output and input to JSON based data
from random import randint	# Used to Randomly generate the time to wait between the requests
from time import sleep		# Function used to pause the program to allow for some wait time between requests
import datetime				# Module Used for Date related functions 
import codecs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

class Nsgclass:
	"""
	Class Created that reads in a given textfile and processes the sentiment analysis on that returning a dict object
	"""
	def __init__(self, name, **kwargs):
		self.name = name                        # Name Provided for Logging Purposes 
		self.base =  str(os.path.dirname(os.path.abspath( __file__ )))
		for key in kwargs:
			# This will look at different Given Arguments Passed by a Class and process them accordingly
			if str(key).lower() == 'given_argument':
				pass
			elif str(key).lower() == 'logging':
				# The following says an argument was given where the user asked for Logging to be True
				# The following action is depricated to allow for the logging that Teradata Module Does.
				if str(kwargs[key]).lower() == "file":
					try:  # Catch Block to create a self logging instance as this is extremely Important to Submit Success or Failure
						if not os.path.exists( self.base + "/logs"):
							os.makedirs(self.base + "/logs")
						self.log = self.createLog(	application=str(self.name),
													applicationpath=str(self.base + '/logs/{}.log'.format(self.name)))
					except Exception as error:
						# The following will Raise a better error that lets us unstand it was caused by Logging Module
						raise ValueError("Not Able to Initiate Log File: {}".format(error))
				elif str(kwargs[key]).lower() == "std":
					try:  # Catch Block to create a self logging instance as this is extremely Important to Submit Success or Failure
						self.log = self.createLog(	application=str(self.name),
													applicationpath=str(self.base + '/logs/{}.log'.format(self.name)),
													stdOutput = True, fileOutput = False)
					except Exception as error:
						# The following will Raise a better error that lets us unstand it was caused by Logging Module
						raise ValueError("Not Able to Initiate Log File: {}".format(error))
				elif str(kwargs[key]).lower() == "both":
					try:  # Catch Block to create a self logging instance as this is extremely Important to Submit Success or Failure
						if not os.path.exists( self.base + "/logs"):
							os.makedirs(self.base + "/logs")
						self.log = self.createLog(	application=str(self.name),
													applicationpath=str(self.base + '/logs/{}.log'.format(self.name)),
													stdOutput = True)
					except Exception as error:
						# The following will Raise a better error that lets us unstand it was caused by Logging Module
						raise ValueError("Not Able to Initiate Log File: {}".format(error))
				
	def createLog(self, application, applicationpath, fileOutput = True, fileRotate = False, stdOutput = False):
		"""
		Base Logging Function created to write output from various functions for better error checking
		this function is for class use only and not meant to be used by outside user.\n
		
		@param  application  (str)   Name of the Logging Instance that is to be created\n
		@param  applicationpath  (str)   Path of the Logging file to which this information will be appended\n
		@param	fileOutput	(bool)	Flag to let users write log output to file
		@param	fileRotate	(bool)	Flag to set Log File Rotation in place
		@param	stdOutput	(bool)	Flag to let users stream output to standard out
		@return mylog   (loggingClass)    Logging Class instance used to write to the log file.\n
		"""
		#fileRotate = False					# Will Implement a file Rotation Policy for Logs
		mylog = logging.getLogger(application)
		if fileOutput == True:
			# If the file Rotating Flag is On then we will 
			if fileRotate == True:
				fileHandler = logging.RotatingFileHandler(applicationpath, maxBytes = (1048576*5), backupCount = 7)
				fileHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s'))
			else:
				fileHandler = logging.FileHandler(applicationpath)
				fileHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s'))
			mylog.addHandler(fileHandler)
		if stdOutput == True:			# If the Output 
			consoleHandler = logging.StreamHandler()
			consoleHandler.setFormatter(logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s'))
			mylog.addHandler(consoleHandler)
		mylog.setLevel(logging.DEBUG)
		return mylog

	def createCSVFromList(self, titleList, dataArrays, fileName):
		"""
		This take the downloaded and formatted data and create an csv file

		@param	titleList	(list)	List of titles for csv file ex, ["index", "name", "movie"]
		@param	dataArrays	(list)	List of Lists of data that will be added to array\
			EX: [ ["Data 1", "Data 2", "Data3"],  ["Data 1", "Data 2", "Data3"]]
		@param	fileName	(str)	Name of the csv file we will write to
		"""
		# This checks to see the filename has already not be created
		if not os.path.isfile(self.base + "/" + fileName + ".csv"):
			fileToOpen = self.base + "/" + fileName + ".csv"
		# This will execute if filename already exists
		else:
			# I will be adding Timestamp to FileName Provided to allow for Multiple Files to exist
			# And no file to be overwritten
			fileToOpen = (	self.base + "/" + fileName + 
							datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".csv" )
		with open(fileToOpen, 'w') as outputFile:
			# Will Looks to see that the Title Array Matches the Second List of Data Array
			# To make sure we can write the columns as we expect
			if len(titleList) == len(dataArrays[0]):
				# Writes each element of header to be processes using List Comprehension Style
				outputFile.write(','.join('"{}"'.format(csvHeader) for csvHeader in titleList)+ "\n")
				for dataArray in dataArrays:
					outputFile.write(','.join('"{}"'.format(csvData) for csvData in dataArray)+ "\n" )
			else:
				error = "We have a mismatch in Titles and Data Arrays, TitleArray: {}, DataArray:{}".format( len(titleList),
																											 len(dataArrays[0]))
				self.log.error(error)
				raise ValueError(error)
	
	def createTabbedTextFileFromList(self, dataArrays, fileName):
		"""
		This takes the downloaded and formatted data and create an tabbed file

		@param	dataArrays	(list)	List of Lists of data that will be added to array\
			EX: [ ["Data 1", "Data 2", "Data3"],  ["Data 1", "Data 2", "Data3"]]
		@param	fileName	(str)	Name of the csv file we will write to
		"""
		# This checks to see the filename has already not be created
		if not os.path.isfile(self.base + "/" + fileName ):
			fileToOpen = self.base + "/" + fileName 
		# This will execute if filename already exists
		else:
			# I will be adding Timestamp to FileName Provided to allow for Multiple Files to exist
			# And no file to be overwritten
			fileToOpen = (	self.base + "/" + fileName + 
							datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") )
		with open(fileToOpen, 'w') as outputFile:
			for dataArray in dataArrays:
				outputFile.write('\t'.join('"{}"'.format(tabbedData) for tabbedData in dataArray) + "\n" )
	
	def loadData(self, fileName, **kwargs):
		"""
		This Function opens up formatted files and returns lists of Data to process results as needed

		@param  fileName    (str)   Name of the file that needs to be opened up to be processed
		"""
		#Local Function Variables that will be returned
		rawData =[]             # Returned Data List(s) - Data Columns 
		rawDataLabels =[]       # Returned Data List - Label Columns
		tabbedFile = False      # If the file being read in is a simple tabbed file   
		csvFile = False         # If the file being read in is a complex csv file
		dataColumns = []        # Column Names of the Data that algorithm will be using
		labelColumns = []       # The lable that the data should be diriving
		# Reading in the arguments provided by the function
		for key in kwargs:
			# This will look at different Given Arguments Passed by a Class and process them accordingly
			if str(key).lower() == 'given_argument':
				pass
			elif str(key).lower() == 'tabbedfile':
				tabbedFile = kwargs[key]
			elif str(key).lower() == 'csvfile':
				csvFile = kwargs[key]
			elif str(key).lower() == 'returnlabelcolumns':
				labelColumns = kwargs[key]
			elif str(key).lower() == 'returndatacolumns':
				dataColumns = kwargs[key]
		# Opening Up file to retun the processed Data Objects
		if tabbedFile == True:
			with codecs.open(fileName, 'r',  encoding='utf-8', errors='ignore' ) as inputFile:
				for line in inputFile.readlines():
					try:
						rawDataObj, rawDataLabel = line.strip().split('\t')
						rawData.append(rawDataObj.lower())
						rawDataLabels.append(rawDataLabel.lower())
					except Exception as error:
						self.log.error("Could not parse this line from {} line {}, error {}".format(fileName, line, error))
			return  rawDataLabels, rawData
		# Now if we are reading in a file that is a csv file, we will use Pandas
		if csvFile == True:
			myDF = pandas.read_csv(fileName ) #, index_col = False)
			#print(myDF)
			rawDataLabelsList = myDF[labelColumns].values.tolist()
			rawDataList = myDF[dataColumns].values.tolist()
			for element in rawDataLabelsList:
				try:
					rawDataLabels.append(element[0])
				except Exception as error:
					self.log.error("Received Issue loading Data from {}: for Labels, error {}".format(fileName, error))

			for element in rawDataList:
				try:
					rawData.append(element[0])
				except Exception as error:
					self.log.error("Received Issue loading Data from {}: for Labels, error {}".format(fileName, error))
			return rawData, rawDataLabels

	def trainModel(self, **kwargs):
		"""
		Will do the model training
		"""
		# Local Variables known to the function Only
		revTrain = []
		labelsTrain = []
		revTest = []
		labelsTest = []
		algo = "linear"
		# Reading in Keyword Arguments as passed by user
		for key in kwargs:
			# This will look at different Given Arguments Passed by a Class and process them accordingly
			if str(key).lower() == 'given_argument':
				pass
			elif str(key).lower() == 'traindata':
				revTrain = kwargs[key]
			elif str(key).lower() == 'trainlabel':
				labelsTrain = kwargs[key]
			elif str(key).lower() == 'testdata':
				revTest = kwargs[key]
			elif str(key).lower() == 'testlabel':
				labelsTest = kwargs[key]
			elif str(key).lower() == 'algo':
				algo = kwargs[key]
		
		#rev_train,labels_train=self.loadData('TRAIN_DATA')
		#rev_test,labels_test=self.loadData('TEST_DATA')
		#print(revTrain)
		#print(len(revTrain))
		#Build a counter based on the training dataset
		if algo == 'linear':
			clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
		elif algo == "svm":
			clf = SVC(gamma=0.001, decision_function_shape='ovo')
		elif algo == "mlp":
			clf = MLPClassifier(alpha=.001, learning_rate="adaptive", learning_rate_init=0.001, early_stopping=False, max_iter=1000, verbose =True)
		elif algo == 'knn':
			clf = KNeighborsClassifier(n_neighbors = 15)
		elif algo == 'tree':
			clf = DecisionTreeClassifier()

		counter = CountVectorizer()
		counter.fit(revTrain)
		print("Length of Test Data:{} Labels:{}, Train Data:{} Labels:{}".format(   len(revTest),
																					len(labelsTest),  
																					len(revTrain), 
																					len(labelsTrain)))

		#count the number of times each term appears in a document and transform each doc into a count vector
		countsTrain = counter.transform(revTrain)#transform the training data
		countsTest = counter.transform(revTest)#transform the testing data

		#train classifier
		#clf = DecisionTreeClassifier()
		# clf = LogisticRegression()
		#clf = MLPClassifier()
		#train all classifier on the same datasets
		clf.fit(countsTrain,labelsTrain)

		#use hard voting to predict (majority voting)
		pred=clf.predict(countsTest)

		#print accuracy
		algoAccuracy = accuracy_score(pred,labelsTest)
		self.log.info("Accuracy of the Model {}".format(algoAccuracy))

if __name__ == '__main__':
	# For your own log file to avoid merge conflicts = Name the class something else
	workerClass = Nsgclass(name = "FinalOutput", logging="Both")
	"""
	workerClass.log.info("Inital Run with files than have no more than 1000 records and have 5 unique features")
	# Load Data 
	testData, testLabel = workerClass.loadData( fileName = 'Test',
												tabbedFile = True)
	trainData, trainLabel = workerClass.loadData(   fileName = 'Train',
													tabbedFile = True)
	workerClass.log.info("Running Linear Regression Algorithm")
	workerClass.trainModel( algo = 'linear',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	workerClass.log.info("Running SVM Algorithm")
	workerClass.trainModel( algo = 'svm',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	workerClass.log.info("Running MLP Algorithm")
	workerClass.trainModel( algo = 'mlp',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	workerClass.log.info("Running Decision Tree Algorithm")
	workerClass.trainModel( algo = 'tree',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	workerClass.log.info("Running KNN Neighbors Algorithm")
	workerClass.trainModel( algo = 'knn',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	"""
	from fixUpDataSets import DataPrep
	workerClass2 = DataPrep(name = "DP_Testing", logging = "both")
	fileNames = workerClass2.makeTestTrainFiles(	fileNames = ['dataSetOriginal/articles2.csv', 'dataSetOriginal/articles1.csv'],
													columnNames = ['publication', 'content'],
													numOfFeatures = 4,
													numOfRecPerFile = 10000,
													featureCol = 'publication',
													returnTabbed = True)
	# Load Data 2 Time with 10,000 Record Files 
	testData, testLabel = workerClass.loadData( fileName = fileNames[0],
												tabbedFile = True)
	trainData, trainLabel = workerClass.loadData(   fileName = fileNames[1],
													tabbedFile = True)
	workerClass.log.info("Running Linear Regression Algorithm")
	workerClass.trainModel( algo = 'linear',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	workerClass.log.info("Running SVM Algorithm")
	workerClass.trainModel( algo = 'svm',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	workerClass.log.info("Running MLP Algorithm")
	workerClass.trainModel( algo = 'mlp',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	workerClass.log.info("Running Decision Tree Algorithm")
	workerClass.trainModel( algo = 'tree',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)
	workerClass.log.info("Running KNN Neighbors Algorithm")
	workerClass.trainModel( algo = 'knn',
							trainData = trainData,
							trainLabel = trainLabel,
							testData = testData,
							testLabel = testLabel)