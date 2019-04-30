#########################################################################
# Khuram Chughtai
# Web Mining Class
# Exploring all-the-news Dataset
# https://www.kaggle.com/snapcrack/all-the-news/version/4#_=_
# 143,000 Articles from 15 different publications"

#Libraries Imported to help with processing data
import pandas
import numpy
import logging


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

    def makeTestTrainFiles(self, fileNames, **kwargs):
        """
        This function will read in the raw data files and parse them accordingly to create test and train datasets
        """
        # Global Variables
        listOfDataFrames = []
        listOfColumns
        self.log.info("Starting to Read file to create Test and Train Data Files formatting them as needed")
        self.log.info("Received the following fileNames for the raw files to create test and train data from: {}".format(fileNames))
        for fileName in fileNames:
            # For Each Data Record within this scope already has an index so it will be redundant to include another index and waste
            # of computer resources making another column
            listOfDataFrames.append(pandas.read_csv(filepath_or_buffer = fileName, index_col= false))




if __name__ == '__main__':
	workerClass = WordScraper(name = "Week5", logging=True)
	myTagger = nltk.load('taggers/maxent_treebank_pos_tagger/english.pickle')

	# When Read in From File
	text = workerClass.readFile(fileName = "input.txt")
	
    positiveWords = workerClass.createListFromFile(fileName = "positive-words.txt")
	negativeWords = workerClass.createListFromFile(fileName = "negative-words.txt")

	sentences = nltk.sent_tokenize(text)

	for sentence in sentences:
		print(workerClass.processSentence( 	sentence=sentence.lower(),
											posLex = positiveWords,
											negLex = negativeWords,
											tagger = myTagger))
