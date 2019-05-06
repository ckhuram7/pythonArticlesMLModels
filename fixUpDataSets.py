#########################################################################
# Khuram Chughtai
# Web Mining Class
# Exploring all-the-news Dataset
# https://www.kaggle.com/snapcrack/all-the-news/version/4#_=_
# 143,000 Articles from 15 different publications"

#Libraries Imported to help with processing data
import pandas
import os
import numpy
import logging
import datetime
import codecs

class DataPrep:
	"""
	Class Created that reads in a given textfile and processes the sentiment analysis on that returning a dict object
	"""
	def __init__(self, name, **kwargs):
		self.name = name
		self.base =  str(os.path.dirname(os.path.abspath( __file__ )))
		self.wordFreqDict = []
		#Initalizing TeraData Connection
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

	def createListFromFile(self, fileName):
		"""
		Takes an input of Filename and reads the given file and splits it into a list of lines to be processed.  
		@param fileName (str)  The file name to open in current directory to processs

		returns list of lines from the file
		"""
		try:
			with open(self.base + "/" + fileName, 'r') as inputFile:
				myListOfLines = inputFile.read().splitlines()
				self.log.info("Read in from: {} and created a list of {} elements".format(fileName, len(myListOfLines)))
				return myListOfLines
		except Exception as error:
			self.log.error("Could not parse file: {}".format(error))

	def readFile(self, fileName):
		"""
		Takes an input of Filename and reads the given file and splits it into a list of lines to be processed.  
		
		@param fileName (str)  The file name to open in current directory to processs
		"""
		try:
			with open(self.base + "/" + fileName, 'r') as inputFile:
				return inputFile.read()
		except Exception as error:
			self.log.error("Could not parse file: {}".format(error))

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
			fileToOpen = (	 fileName + datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") )
		with codecs.open(self.base + "/" + fileToOpen, 'w', encoding='utf-8', errors='ignore') as outputFile:
			for dataArray in dataArrays:
				try:
					outputFile.write('\t'.join('"{}"'.format(tabbedData.strip().replace('\t', '')) for tabbedData in dataArray) + "\n" )
				except Exception as error:
					self.log.error("Could not write line to file: {}".format(str(dataArray)))
		return fileToOpen

	def splitRecords(self, numToBalance, numOfBots):
		"""
		This function will trying to split the records to process as evenly as possible based of the number of bots provided 
		and creates a list that gives how many records each bot should end up running.

		@param  numToBalance    (int)   The number of records that the overall project has to run
		@param  numOfBots   (int)   The number of bots that are running that need to have the records split amongst
		"""
		# List of Values that need to be returned letting the user know how many records to process for each bot
		listToReturn = []
		# Checking if the number Divides up evenly, if it does than it will return a list of how many records each bot should have
		if (numToBalance % numOfBots) == 0:
			# Will Go through the number of Bots that need to run to slit records as evenly as possible
			for value in range(numOfBots):
				listToReturn.append(numToBalance // numOfBots)
		# This will process if the numbers do not divde evenly and we need to split records unevenly 
		else:
			# Will Go through the number of Bots that need to run to slit records as evenly as possible
			for value in range(numOfBots):
				# If the remainder is more than the bot number to be splitting the records for
				if (numToBalance % numOfBots) > value:
					listToReturn.append((numToBalance // numOfBots) + 1)
				# If the remainder is less than the bot number to be splitting the records for
				else:
					listToReturn.append(numToBalance // numOfBots)
		return (listToReturn)

	def makeTestTrainFiles(self, fileNames, **kwargs):
		"""
		This function will read in the raw data files and parse them accordingly to create test and train datasets

		@param  fileNames   (list)  List of files with articles that need to be read in
		@param  columnNames (list)  List of Column Names that should be kept from the file that is read in
		@param  numOfFeatures   (int)   This is the number of the different features that should be returned
		@param	specificFeatures	(list)	This is a list of the specific features that we will be using
		@param  featureCol  (str)   The column name that will be used as a feature that we will be testing for and training on
		@param  numOfRecPerFile (int)   THe number of rows that each file created will have
		@param	outputFileNames (list)	This will include the outputFileNames 
		@param	returnDFs	(bool)	If this is True than it will return the dataFrames instead of fileNames
		@param	returnTabbed	(bool)	If this is True than it will return tabbed files instead of csv files
		@param  removeStopwords (bool)  If true will remove all stop words from articles
		"""
		# Local Function Variables
		listOfDataFrames = []
		listOfColumns = []
		numOfFeatures = 5
		featureCol = ''
		numOfRecPerFile = 1000
		outputFileNames = [	"Train_" + datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".csv",
							"Test_"  + datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"]
		returnDF = False
		returnTabbed = False
		# Reading in the arguments provided by the function
		for key in kwargs:
			# This will look at different Given Arguments Passed by a Class and process them accordingly
			if str(key).lower() == 'given_argument':
				pass
			elif str(key).lower() == 'columnnames':
				listOfColumns = kwargs[key]
			elif str(key).lower() == 'numoffeatures':
				numOfFeatures = kwargs[key]
			elif str(key).lower() == 'featurecol':
				featureCol = kwargs[key]
			elif str(key).lower() == 'numofrecperfile':
				numOfRecPerFile = kwargs[key]
			elif str(key).lower() == 'outputfilenames':
				outputFileNames  = kwargs[key]
			elif str(key).lower() == 'returndf':
				returnDF  = kwargs[key]
			elif str(key).lower() == 'returntabbed':
				returnTabbed  = kwargs[key]

		self.log.info("Starting to Read file to create Test and Train Data Files formatting them as needed")
		self.log.info("Received the following fileNames for the raw files to create test and train data from: {}".format(fileNames))
		for fileName in fileNames:
			# For Each Data Record within this scope already has an index so it will be redundant to include another index and waste
			# of computer resources making another column
			listOfDataFrames.append(pandas.read_csv(filepath_or_buffer = fileName, index_col= False))
		
		# Now to Concat the list of DataFrames if there is more than one.
		if len(fileNames) > 1:
			self.log.info("Since more than one file was given, using pandas concat function to combine files into one DataFrame")
			opsDF = pandas.concat(listOfDataFrames)
		else:
			#Will Go Into this test If the size of the DataFrame is 1 or less
			opsDF = listOfDataFrames[0]
		self.log.info("Generated Dataframe has the following dimensions: {}".format(str(opsDF.shape)))
		self.log.info("Generated Dataframe columns: {}".format(str(opsDF.columns)))
		
		# Now that we have the given fileName we will reduce the numberOfColumns to the column list provided
		#Checking to see if provided argument has a length greater than 0
		if len(listOfColumns) > 0:
			# Making sure that the list of Columns is not greater than what we expect to have from DataFrame
			if len(listOfColumns) < len(opsDF.columns):
				# Checking to see all of the required columns are present in the DataFrame
				if set(listOfColumns).issubset(opsDF.columns):
					opsDF = opsDF[listOfColumns]
				else:
					self.log.error("Failure when checking if listOfColumns exist in pandas DataFrame: {}".format(set(listOfColumns).issubset(opsDF.columns)))
					raise IndexError("Not all elements requested are part of pandas Dataframe")
		# else: # This wont be needed as any records that do not fit above means original DataFrame will be used
		# This Portion we will be using all of the DataFrame columns that are provided
		
		# We first at if the feature column exists 
		if featureCol in opsDF.columns.tolist(): 
			# This is to extract the total number of features that are available
			featureCounts = [ 	opsDF[featureCol].value_counts().keys().tolist(),
								opsDF[featureCol].value_counts().tolist()	]

			self.log.info("Counts of Different features that exist in the dataFrame: {}".format(str(featureCounts)))
			# Now we Check to see if we have enough features to meet the number of different features requested
			# Due to the way we have retrevied the information we need to check first element list to verify the count
			# of different records that exist in new dataFrame
			if numOfFeatures <= len(featureCounts[0]):
				# We Multiply by Two to allow for easier split between Train and Test Records
				sampleSize = self.splitRecords( numToBalance = (numOfRecPerFile * 2), numOfBots=numOfFeatures)
				self.log.info("Proposed Numbers to Split Records evenly: {}".format(sampleSize))
				listOfSampleDFs = []	# Split Samples Records - TO make sure there is no overlap
				listOfTrainDFs = []		# Records Split to include only the Training Data for File Creation
				listOfTestDFs = []		# Records Split to include only the Testing Data for File Creation
				# We will Check through and sample each of the minor dfs which only include the column record we are looking for
				# Once it parses that it will make sure the records are evenly split
				for iterObj, sizePull in enumerate(sampleSize):
					listOfSampleDFs.append( (opsDF.loc[opsDF[featureCol] == featureCounts[0][iterObj]]).sample(n=sizePull) )
					self.log.info("Shape of Split DF {}, Split on {} == {}, Out Of {} possible records".format(	str(listOfSampleDFs[iterObj].shape), 
																												featureCol,
																												featureCounts[0][iterObj],
																					 							featureCounts[1][iterObj]))
				# Now we will Split the records as evenly as possible
				for iterObj, sampleDF in enumerate(listOfSampleDFs):
					sliceInt = int(sampleDF.shape[0] / 4) * 3
					#sliceIntSecond = sliceInt / 2 
					listOfTestDFs.append(sampleDF[:sliceInt])
					listOfTrainDFs.append(sampleDF[sliceInt:])
					self.log.info("Train Sub DF shape {}, Split on {} == {}, Out Of {} possible records".format(str(listOfTrainDFs[iterObj].shape), 
																												featureCol,
																												featureCounts[0][iterObj],
																												featureCounts[1][iterObj]) )
					self.log.info("Test Sub DF shape {}, Split on {} == {}, Out Of {} possible records".format(	str(listOfTestDFs[iterObj].shape), 
																												featureCol,
																												featureCounts[0][iterObj],
																												featureCounts[1][iterObj]) )
				# Concatting the SubDivided DataFrames into One
				testDF = pandas.concat(listOfTestDFs)
				trainDF = pandas.concat(listOfTrainDFs)

				# Outputting Files to CSV
				if returnDF == True:
					testDF.to_csv( 	outputFileNames[1],	index = False)
					trainDF.to_csv(	outputFileNames[0],	index = False)
				elif returnTabbed == True:
					outputFileNames[0] = self.createTabbedTextFileFromList(	fileName = "Train",
																			dataArrays = trainDF.values.tolist())
					outputFileNames[1] = self.createTabbedTextFileFromList(	fileName = "Test",
																			dataArrays = testDF.values.tolist())
			else:
				raise ValueError("Not enough different features to meet requirements: Requested {}, Available {}".format(numOfFeatures, len(featureCounts[0])))
		else:
			raise IndexError("Feature Column {} not in Dataframe {}".format(featureCol, str(opsDF.columns)))
		
		# This is working on the Return portion of the Function
		if returnDF == True:
			self.log.info("Return DataFrames, DF 1 Shape {}, DF 2 Shape {}".format(	str(testDF.shape), 
																					str(trainDF.shape)))
			return [testDF, trainDF]
		else:
			# Returning FileNames which are created
			self.log.info("Created Files, File 1 {}, File 2 {}".format(	outputFileNames[0],
																		outputFileNames[1]))
			return outputFileNames


if __name__ == '__main__':
	workerClass = DataPrep(name = "DP_Testing", logging = "both")
	workerClass.makeTestTrainFiles(	fileNames = ['dataSetOriginal/articles2.csv'],
									columnNames = ['publication', 'content'],
									numOfFeatures = 5,
									numOfRecPerFile = 1000,
									featureCol = 'publication',
									returnTabbed = True)

